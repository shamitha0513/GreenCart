from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    Plant, Category, Order, OrderItem, Payment, User, 
    DeliveryPartner, Service, ServiceBooking, Address
)
from app.utils import admin_required, save_uploaded_image, generate_csv_response

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_plants = Plant.query.count()
    total_orders = Order.query.count()
    total_customers = User.query.filter_by(role='CUSTOMER').count()
    total_delivery_partners = User.query.filter_by(role='DELIVERY_PARTNER').count()
    
    successful_payments = Payment.query.filter_by(payment_status='Successful').all()
    total_revenue = sum(p.amount for p in successful_payments)
    
    pending_orders = Order.query.filter(Order.order_status.in_(['Placed', 'Confirmed', 'Assigned', 'Accepted', 'Out for Delivery'])).count()
    delivered_orders = Order.query.filter_by(order_status='Delivered').count()
    
    # Low stock alert plants (stock <= 5)
    low_stock_plants = Plant.query.filter(Plant.stock_quantity <= 5).order_by(Plant.stock_quantity.asc()).all()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                           total_plants=total_plants,
                           total_orders=total_orders,
                           total_customers=total_customers,
                           total_delivery_partners=total_delivery_partners,
                           total_revenue=total_revenue,
                           pending_orders=pending_orders,
                           delivered_orders=delivered_orders,
                           low_stock_plants=low_stock_plants,
                           recent_orders=recent_orders)

# Chart Data REST Endpoint
@admin_bp.route('/chart-data')
@login_required
@admin_required
def chart_data():
    # Category sales breakdown
    categories = Category.query.all()
    cat_names = [c.name for c in categories]
    cat_sales = []
    
    for cat in categories:
        sales_count = db.session.query(db.func.sum(OrderItem.quantity))\
            .join(Plant, OrderItem.plant_id == Plant.id)\
            .filter(Plant.category_id == cat.id).scalar() or 0
        cat_sales.append(sales_count)
        
    # Order Status breakdown
    statuses = ['Placed', 'Confirmed', 'Assigned', 'Accepted', 'Out for Delivery', 'Delivered', 'Cancelled']
    status_counts = [Order.query.filter_by(order_status=st).count() for st in statuses]
    
    # Top 5 selling plants
    top_items = db.session.query(
        OrderItem.plant_name, 
        db.func.sum(OrderItem.quantity).label('total_qty')
    ).group_by(OrderItem.plant_name).order_by(db.desc('total_qty')).limit(5).all()
    
    top_plant_names = [item[0] for item in top_items]
    top_plant_qtys = [item[1] for item in top_items]
    
    return jsonify({
        'categories': cat_names,
        'category_sales': cat_sales,
        'statuses': statuses,
        'status_counts': status_counts,
        'top_plants': top_plant_names,
        'top_plant_qtys': top_plant_qtys
    })

# --- Plant Management ---
@admin_bp.route('/plants')
@login_required
@admin_required
def plants():
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '').strip()
    
    query = Plant.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search_query:
        query = query.filter((Plant.name.ilike(f'%{search_query}%')) | (Plant.scientific_name.ilike(f'%{search_query}%')))
        
    all_plants = query.order_by(Plant.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('admin/plants.html', plants=all_plants, categories=categories, selected_category=category_id, search_query=search_query)

@admin_bp.route('/plant/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_plant():
    categories = Category.query.all()
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        name = request.form.get('name').strip()
        scientific_name = request.form.get('scientific_name', '').strip()
        description = request.form.get('description').strip()
        benefits = request.form.get('benefits', '').strip()
        care_instructions = request.form.get('care_instructions', '').strip()
        sunlight = request.form.get('sunlight', 'Partial Shade')
        water_requirement = request.form.get('water_requirement', 'Weekly')
        soil_type = request.form.get('soil_type', 'Well-draining pot mix')
        size = request.form.get('size', 'Medium')
        price = float(request.form.get('price'))
        discount = float(request.form.get('discount', 0.0))
        stock_quantity = int(request.form.get('stock_quantity', 10))
        image_url_input = request.form.get('image_url', '').strip()
        
        # Handle file upload or image URL
        image_file = request.files.get('image_file')
        image_path = save_uploaded_image(image_file) if image_file and image_file.filename else None
        
        if not image_path:
            image_path = image_url_input or 'images/plants/indoor/snake_plant.jpg'
            
        new_plant = Plant(
            category_id=category_id,
            name=name,
            scientific_name=scientific_name,
            description=description,
            benefits=benefits,
            care_instructions=care_instructions,
            sunlight=sunlight,
            water_requirement=water_requirement,
            soil_type=soil_type,
            size=size,
            price=price,
            discount=discount,
            stock_quantity=stock_quantity,
            image=image_path,
            status='ACTIVE' if stock_quantity > 0 else 'OUT_OF_STOCK'
        )
        db.session.add(new_plant)
        db.session.commit()
        
        flash(f'Plant "{name}" added successfully!', 'success')
        return redirect(url_for('admin.plants'))
        
    return render_template('admin/plant_form.html', categories=categories, plant=None)

@admin_bp.route('/plant/edit/<int:plant_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        plant.category_id = request.form.get('category_id', type=int)
        plant.name = request.form.get('name').strip()
        plant.scientific_name = request.form.get('scientific_name', '').strip()
        plant.description = request.form.get('description').strip()
        plant.benefits = request.form.get('benefits', '').strip()
        plant.care_instructions = request.form.get('care_instructions', '').strip()
        plant.sunlight = request.form.get('sunlight')
        plant.water_requirement = request.form.get('water_requirement')
        plant.soil_type = request.form.get('soil_type')
        plant.size = request.form.get('size')
        plant.price = float(request.form.get('price'))
        plant.discount = float(request.form.get('discount', 0.0))
        plant.stock_quantity = int(request.form.get('stock_quantity'))
        
        image_url_input = request.form.get('image_url', '').strip()
        image_file = request.files.get('image_file')
        
        if image_file and image_file.filename:
            uploaded_path = save_uploaded_image(image_file)
            if uploaded_path:
                plant.image = uploaded_path
        elif image_url_input:
            plant.image = image_url_input
            
        plant.status = 'ACTIVE' if plant.stock_quantity > 0 else 'OUT_OF_STOCK'
        db.session.commit()
        
        flash(f'Plant "{plant.name}" updated successfully!', 'success')
        return redirect(url_for('admin.plants'))
        
    return render_template('admin/plant_form.html', categories=categories, plant=plant)

@admin_bp.route('/plant/delete/<int:plant_id>', methods=['POST'])
@login_required
@admin_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    name = plant.name
    db.session.delete(plant)
    db.session.commit()
    flash(f'Plant "{name}" deleted successfully.', 'success')
    return redirect(url_for('admin.plants'))

@admin_bp.route('/plant/update-stock/<int:plant_id>', methods=['POST'])
@login_required
@admin_required
def update_stock(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    new_stock = int(request.form.get('stock_quantity', 10))
    plant.stock_quantity = new_stock
    if plant.stock_quantity > 0:
        plant.status = 'ACTIVE'
    db.session.commit()
    flash(f'Stock for {plant.name} updated to {new_stock}.', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/plant/quick-update-image/<int:plant_id>', methods=['POST'])
@login_required
@admin_required
def quick_update_image(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    image_url_input = request.form.get('image_url', '').strip()
    image_file = request.files.get('image_file')
    
    if image_file and image_file.filename:
        uploaded_path = save_uploaded_image(image_file)
        if uploaded_path:
            plant.image = uploaded_path
            db.session.commit()
            flash(f'Image for "{plant.name}" updated successfully via upload!', 'success')
            return redirect(request.referrer or url_for('admin.plants'))
            
    if image_url_input:
        plant.image = image_url_input
        db.session.commit()
        flash(f'Image for "{plant.name}" updated successfully via URL/path!', 'success')
    else:
        flash('Please select an image file or enter an image URL/path.', 'warning')
        
    return redirect(request.referrer or url_for('admin.plants'))

# --- Category Management ---
@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def categories():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name').strip()
            description = request.form.get('description', '').strip()
            slug = name.lower().replace(' ', '-')
            
            if Category.query.filter_by(name=name).first():
                flash(f'Category "{name}" already exists.', 'warning')
            else:
                new_cat = Category(name=name, description=description, slug=slug)
                db.session.add(new_cat)
                db.session.commit()
                flash(f'Category "{name}" added.', 'success')
                
        elif action == 'edit':
            cat_id = request.form.get('category_id', type=int)
            cat = Category.query.get_or_404(cat_id)
            cat.name = request.form.get('name').strip()
            cat.description = request.form.get('description', '').strip()
            cat.slug = cat.name.lower().replace(' ', '-')
            db.session.commit()
            flash('Category updated.', 'success')
            
        return redirect(url_for('admin.categories'))
        
    cats = Category.query.all()
    return render_template('admin/categories.html', categories=cats)

@admin_bp.route('/category/delete/<int:cat_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    if cat.plants:
        flash(f'Cannot delete category "{cat.name}" because it contains {len(cat.plants)} plants. Reassign or delete plants first.', 'danger')
    else:
        db.session.delete(cat)
        db.session.commit()
        flash(f'Category "{cat.name}" deleted.', 'success')
    return redirect(url_for('admin.categories'))

# --- Order Management & Delivery Partner Assignment ---
@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    status_filter = request.args.get('status', '')
    query = Order.query
    if status_filter:
        query = query.filter_by(order_status=status_filter)
        
    all_orders = query.order_by(Order.created_at.desc()).all()
    delivery_partners = User.query.filter_by(role='DELIVERY_PARTNER', status='ACTIVE').all()
    
    return render_template('admin/orders.html', 
                           orders=all_orders, 
                           delivery_partners=delivery_partners,
                           selected_status=status_filter)

@admin_bp.route('/order/update/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    action = request.form.get('action')
    
    if action == 'confirm':
        order.order_status = 'Confirmed'
        flash(f'Order #{order.id} confirmed.', 'success')
    elif action == 'assign_partner':
        dp_id = request.form.get('delivery_partner_id', type=int)
        if dp_id:
            order.delivery_partner_id = dp_id
            order.order_status = 'Assigned'
            flash(f'Delivery Partner assigned to Order #{order.id}.', 'success')
    elif action == 'cancel':
        order.order_status = 'Cancelled'
        # Restores stock on order cancellation (PDF requirement 49 rule 8)
        for item in order.items:
            item.plant.stock_quantity += item.quantity
            if item.plant.stock_quantity > 0:
                item.plant.status = 'ACTIVE'
        flash(f'Order #{order.id} cancelled and stock restored.', 'info')
        
    db.session.commit()
    return redirect(url_for('admin.orders'))

# --- Payment Reports ---
@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    status_filter = request.args.get('status', '')
    method_filter = request.args.get('method', '')
    
    query = Payment.query
    if status_filter:
        query = query.filter_by(payment_status=status_filter)
    if method_filter:
        query = query.filter_by(payment_method=method_filter)
        
    all_payments = query.order_by(Payment.payment_date.desc()).all()
    
    total_revenue = sum(p.amount for p in all_payments if p.payment_status == 'Successful')
    successful_count = sum(1 for p in all_payments if p.payment_status == 'Successful')
    pending_count = sum(1 for p in all_payments if p.payment_status == 'Pending')
    failed_count = sum(1 for p in all_payments if p.payment_status == 'Failed')
    
    return render_template('admin/payments.html',
                           payments=all_payments,
                           total_revenue=total_revenue,
                           successful_count=successful_count,
                           pending_count=pending_count,
                           failed_count=failed_count)

@admin_bp.route('/payments/export')
@login_required
@admin_required
def export_payments_csv():
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    headers = ['Payment ID', 'Transaction ID', 'Order ID', 'Customer ID', 'Amount (INR)', 'Method', 'Status', 'Date']
    rows = []
    for p in payments:
        rows.append([
            p.id, p.transaction_id, p.order_id, p.user_id, p.amount, p.payment_method, p.payment_status, p.payment_date.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return generate_csv_response(headers, rows, filename="greencart_payment_report.csv")

# --- Reports Module ---
@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    filter_range = request.args.get('range', 'this_month')
    now = datetime.utcnow()
    
    if filter_range == 'today':
        start_date = now.replace(hour=0, minute=0, second=0)
    elif filter_range == 'this_week':
        start_date = now - timedelta(days=now.weekday())
    elif filter_range == 'this_year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0)
    else: # this_month
        start_date = now.replace(day=1, hour=0, minute=0, second=0)
        
    orders = Order.query.filter(Order.created_at >= start_date).all()
    total_sales = sum(o.grand_total for o in orders if o.order_status != 'Cancelled')
    order_count = len(orders)
    
    return render_template('admin/reports.html', 
                           orders=orders, 
                           total_sales=total_sales, 
                           order_count=order_count, 
                           filter_range=filter_range)

# --- Services Management ---
@admin_bp.route('/services', methods=['GET', 'POST'])
@login_required
@admin_required
def services():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_service':
            name = request.form.get('name')
            desc = request.form.get('description')
            price = float(request.form.get('price'))
            new_s = Service(name=name, description=desc, price=price, status='ACTIVE')
            db.session.add(new_s)
            db.session.commit()
            flash('Service added successfully.', 'success')
        elif action == 'update_booking_status':
            booking_id = request.form.get('booking_id', type=int)
            b = ServiceBooking.query.get_or_404(booking_id)
            b.status = request.form.get('status')
            db.session.commit()
            flash('Service booking status updated.', 'success')
            
        return redirect(url_for('admin.services'))
        
    all_services = Service.query.all()
    bookings = ServiceBooking.query.order_by(ServiceBooking.created_at.desc()).all()
    return render_template('admin/services.html', services=all_services, bookings=bookings)
