import os
from flask import Flask, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'media'), exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.models import User, Cart, CartItem
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Custom image URL filter to handle absolute URLs, uploaded media, and local static assets safely
    @app.template_filter('img_url')
    def img_url(path):
        if not path:
            return url_for('static', filename='images/categories/indoor-plants.jpg')
        path_str = str(path).strip().replace('\\', '/')
        if path_str.startswith('http://') or path_str.startswith('https://'):
            return path_str
            
        if path_str.startswith('/static/'):
            clean_path = path_str[8:]
        elif path_str.startswith('static/'):
            clean_path = path_str[7:]
        elif path_str.startswith('/'):
            clean_path = path_str[1:]
        else:
            clean_path = path_str

        # Split path into OS-native disk parts for reliable cross-platform path checks
        disk_parts = [p for p in clean_path.split('/') if p]
        full_disk_path = os.path.join(app.root_path, 'static', *disk_parts)
        
        if os.path.exists(full_disk_path):
            return url_for('static', filename='/'.join(disk_parts))

        # Direct Sibling Check: If requested .svg file, check if .jpg version exists in same directory
        if len(disk_parts) >= 1:
            base_name, ext = os.path.splitext(disk_parts[-1])
            jpg_parts = disk_parts[:-1] + [f"{base_name}.jpg"]
            jpg_full_path = os.path.join(app.root_path, 'static', *jpg_parts)
            if os.path.exists(jpg_full_path):
                return url_for('static', filename='/'.join(jpg_parts))
            
        # Fallback 1: if path points to a missing file or old SVG, check for matching JPG image in plants folder
        filename_only = disk_parts[-1] if disk_parts else ''
        if filename_only:
            plant_name_clean = filename_only.split('.')[0].lower().replace('-', '_')
            plants_dir = os.path.join(app.root_path, 'static', 'images', 'plants')
            if os.path.exists(plants_dir):
                for custom_img in os.listdir(plants_dir):
                    if custom_img.lower().endswith(('.jpg', '.png', '.jpeg')):
                        c_lower = custom_img.lower().replace('-', '_')
                        clean_parts = [p for p in plant_name_clean.split('_') if len(p) > 2]
                        if plant_name_clean in c_lower or (len(clean_parts) >= 2 and all(part in c_lower for part in clean_parts[:2])):
                            return url_for('static', filename=f'images/plants/{custom_img}')

        # Fallback 2: Category SVG default
        return url_for('static', filename='images/categories/indoor-plants.jpg')
        
    # Global context processors for templates
    @app.context_processor
    def inject_global_vars():

        cart_count = 0
        if current_user.is_authenticated and current_user.role == 'CUSTOMER':
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if cart:
                cart_count = sum(item.quantity for item in cart.items)
        return dict(cart_count=cart_count)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.customer import customer_bp
    from app.routes.admin import admin_bp
    from app.routes.delivery import delivery_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(delivery_bp, url_prefix='/delivery')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
        
    @app.errorhandler(403)
    def access_denied(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
        
    return app
