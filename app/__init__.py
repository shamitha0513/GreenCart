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
            return url_for('static', filename='images/categories/indoor-plants.svg')
        path_str = str(path).strip()
        if path_str.startswith('http://') or path_str.startswith('https://'):
            return path_str
        if path_str.startswith('/static/'):
            return path_str
        if path_str.startswith('static/'):
            return '/' + path_str
        return url_for('static', filename=path_str)
        
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
