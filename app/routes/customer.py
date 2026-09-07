import uuid
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import (
    Plant, Category, Cart, CartItem, Order, OrderItem, Payment, 
    Address, Service, ServiceBooking, Review, User
)
from app.utils import customer_required

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
def index():
    featured_plants = Plant.query.filter_by(status='ACTIVE').order_by(Plant.rating.desc()).limit(8).all()
    categories = Category.query.all()
    services = Service.query.limit(4).all()
    return render_template('customer/landing.html', 
                           featured_plants=featured_plants, 
                           categories=categories,
                           services=services)

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_delivery_partner():
        return redirect(url_for('delivery.dashboard'))
        
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    total_orders = len(user_orders)
    active_orders = [o for o in user_orders if o.order_status not in ['Delivered', 'Cancelled']]
    delivered_orders = [o for o in user_orders if o.order_status == 'Delivered']
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    cart_items_count = sum(item.quantity for item in cart.items) if cart else 0
    
    featured_plants = Plant.query.filter_by(status='ACTIVE').order_by(Plant.rating.desc()).limit(4).all()
    new_arrivals = Plant.query.filter_by(status='ACTIVE').order_by(Plant.created_at.desc()).limit(4).all()
    categories = Category.query.limit(6).all()
    
    return render_template('customer/dashboard.html',
                           total_orders=total_orders,
                           active_orders=active_orders,
                           delivered_count=len(delivered_orders),
                           cart_items_count=cart_items_count,
                           featured_plants=featured_plants,
                           new_arrivals=new_arrivals,
                           categories=categories,
                           recent_orders=user_orders[:3])

@customer_bp.route('/plants')
def plants():
    search_query = request.args.get('search', '').strip()
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    availability = request.args.get('availability', '')
    sort_by = request.args.get('sort', 'popular')
    
    query = Plant.query.filter_by(status='ACTIVE')
    
    if search_query:
        query = query.filter(
            (Plant.name.ilike(f'%{search_query}%')) |
            (Plant.scientific_name.ilike(f'%{search_query}%')) |
            (Plant.description.ilike(f'%{search_query}%'))
        )
        
    if category_id:
        query = query.filter(Plant.category_id == category_id)
        
    if min_price is not None:
        query = query.filter(Plant.price >= min_price)
    if max_price is not None:
        query = query.filter(Plant.price <= max_price)
        
    if availability == 'in_stock':
        query = query.filter(Plant.stock_quantity > 0)
    elif availability == 'low_stock':
        query = query.filter(Plant.stock_quantity > 0, Plant.stock_quantity <= 5)
        
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Plant.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Plant.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Plant.created_at.desc())
    elif sort_by == 'rating':
        query = query.order_by(Plant.rating.desc())
    else: # popular
        query = query.order_by(Plant.reviews_count.desc(), Plant.rating.desc())
        
    all_plants = query.all()
    categories = Category.query.all()
    
    return render_template('customer/plants.html', 
                           plants=all_plants, 
                           categories=categories,
                           selected_category=category_id,
                           search_query=search_query,
                           sort_by=sort_by)

@customer_bp.route('/categories')
def categories():
    cats = Category.query.all()
    return render_template('customer/categories.html', categories=cats)

@customer_bp.route('/plant/<int:plant_id>')
def plant_details(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    related_plants = Plant.query.filter(
        Plant.category_id == plant.category_id, 
        Plant.id != plant.id
    ).limit(4).all()
    
    reviews = Review.query.filter_by(plant_id=plant_id).order_by(Review.created_at.desc()).all()
    
    return render_template('customer/details.html', plant=plant, related_plants=related_plants, reviews=reviews)

@customer_bp.route('/suggestions')
def suggestions():
    # Helper to find matching plants by name keywords
    def find_plants(keywords):
        conditions = [Plant.name.ilike(f'%{kw}%') for kw in keywords]
        return Plant.query.filter(db.or_(*conditions)).limit(6).all()

    # Gift categories specified in PDF (Section 14 & prompt)
    gifts = {
        'Birthday Gifts': find_plants(['Rose', 'Orchid', 'Bonsai', 'Echeveria', 'Anthurium', 'Peace Lily', 'Jade']),
        'Housewarming Gifts': find_plants(['Snake', 'Peace Lily', 'Money', 'Jade', 'ZZ Plant', 'Monstera']),
        'Wedding Anniversary Gifts': find_plants(['Rose', 'Jasmine', 'Peace Lily', 'Bonsai', 'Anthurium', 'Flamingo']),
        'Teacher Gifts': find_plants(['Money', 'Peace Lily', 'Aloe', 'Spider', 'Pothos', 'Snake']),
        'Friends Gifts': find_plants(['Succulent', 'Cactus', 'Jade', 'Spider', 'Pearls', 'Haworthia']),
        'Festival Gifts': find_plants(['Tulsi', 'Marigold', 'Bougainvillea', 'Rose', 'Hibiscus', 'Lotus'])
    }
    return render_template('customer/suggestions.html', gift_categories=gifts)

@customer_bp.route('/services', methods=['GET', 'POST'])
def services():
    all_services = Service.query.filter_by(status='ACTIVE').all()
    
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login to book a service.', 'warning')
            return redirect(url_for('auth.login'))
            
        service_id = request.form.get('service_id', type=int)
        booking_date = request.form.get('booking_date')
        address = request.form.get('address')
        notes = request.form.get('notes', '')
        
        if not service_id or not booking_date or not address:
            flash('Please fill in all required service booking details.', 'warning')
            return redirect(url_for('customer.services'))
            
        booking = ServiceBooking(
            service_id=service_id,
            user_id=current_user.id,
            booking_date=booking_date,
            address=address,
            notes=notes,
            status='Pending'
        )
        db.session.add(booking)
        db.session.commit()
        
        flash('Service request submitted successfully! Our team will contact you shortly.', 'success')
        return redirect(url_for('customer.services'))
        
    return render_template('customer/services.html', services=all_services)

@customer_bp.route('/cart')
@login_required
@customer_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
        
    items = cart.items
    subtotal = sum(item.quantity * item.plant.final_price for item in items)
    delivery_fee = 0.0 if subtotal >= 999 or subtotal == 0 else 49.0
    tax = round(subtotal * 0.05, 2) # 5% tax
    grand_total = round(subtotal + delivery_fee + tax, 2)
    
    return render_template('customer/cart.html', 
                           cart=cart, 
                           items=items, 
                           subtotal=subtotal, 
                           delivery_fee=delivery_fee, 
                           tax=tax, 
                           grand_total=grand_total)

@customer_bp.route('/cart/add/<int:plant_id>', methods=['POST'])
@login_required
@customer_required
def add_to_cart(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    quantity = int(request.form.get('quantity', 1))
    
    if plant.stock_quantity <= 0:
        flash('Sorry, this plant is currently out of stock.', 'danger')
        return redirect(request.referrer or url_for('customer.plants'))
        
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, plant_id=plant.id).first()
    
    current_in_cart = cart_item.quantity if cart_item else 0
    if current_in_cart + quantity > plant.stock_quantity:
        flash(f'Cannot add more items than available stock (Stock: {plant.stock_quantity}).', 'warning')
        return redirect(request.referrer or url_for('customer.view_cart'))
        
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            plant_id=plant.id,
            quantity=quantity,
            price=plant.final_price
        )
        db.session.add(cart_item)
        
    db.session.commit()
    flash(f'{plant.name} added to your cart!', 'success')
    
    if request.form.get('buy_now') == '1':
        return redirect(url_for('customer.checkout'))
        
    return redirect(request.referrer or url_for('customer.view_cart'))

@customer_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
@customer_required
def update_cart(item_id):
    action = request.form.get('action') # 'increase', 'decrease', 'remove'
    item = CartItem.query.get_or_404(item_id)
    
    # Check ownership
    if item.cart.user_id != current_user.id:
        flash('Unauthorized cart action.', 'danger')
        return redirect(url_for('customer.view_cart'))
        
    if action == 'increase':
        if item.quantity + 1 > item.plant.stock_quantity:
            flash(f'Cannot exceed available stock level ({item.plant.stock_quantity}).', 'warning')
        else:
            item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
    elif action == 'remove':
        db.session.delete(item)
        
    db.session.commit()
    return redirect(url_for('customer.view_cart'))

@customer_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
@customer_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash('Your cart is empty. Add plants before checking out.', 'warning')
        return redirect(url_for('customer.plants'))
        
    # Verify stock levels before checkout
    for item in cart.items:
        if item.quantity > item.plant.stock_quantity:
            flash(f'Insufficient stock for {item.plant.name}. Only {item.plant.stock_quantity} available.', 'danger')
            return redirect(url_for('customer.view_cart'))
            
    items = cart.items
    subtotal = sum(item.quantity * item.plant.final_price for item in items)
    delivery_fee = 0.0 if subtotal >= 999 else 49.0
    tax = round(subtotal * 0.05, 2)
    grand_total = round(subtotal + delivery_fee + tax, 2)
    
    user_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
    if not user_address:
        user_address = Address.query.filter_by(user_id=current_user.id).first()
        
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address_text = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pincode = request.form.get('pincode')
        payment_method = request.form.get('payment_method', 'UPI')
        
        full_delivery_address = f"{full_name}, {phone}\n{address_text}, {city}, {state} - {pincode}"
        
        # Create Order
        new_order = Order(
            user_id=current_user.id,
            total_amount=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax,
            grand_total=grand_total,
            payment_status='Successful' if payment_method != 'Cash on Delivery' else 'Pending',
            order_status='Placed',
            delivery_address=full_delivery_address
        )
        db.session.add(new_order)
        db.session.flush() # get order.id
        
        # Create OrderItems & AUTOMATIC STOCK REDUCTION
        for item in cart.items:
            order_item = OrderItem(
                order_id=new_order.id,
                plant_id=item.plant_id,
                quantity=item.quantity,
                price=item.plant.final_price,
                plant_name=item.plant.name,
                plant_image=item.plant.image
            )
            db.session.add(order_item)
            
            # Reduce stock automatically (Requirement Section 18)
            item.plant.stock_quantity -= item.quantity
            if item.plant.stock_quantity <= 0:
                item.plant.status = 'OUT_OF_STOCK'
                
        # Create Payment Record
        transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        new_payment = Payment(
            order_id=new_order.id,
            user_id=current_user.id,
            amount=grand_total,
            payment_method=payment_method,
            transaction_id=transaction_id,
            payment_status='Successful' if payment_method != 'Cash on Delivery' else 'Pending'
        )
        db.session.add(new_payment)
        
        # Clear Cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        
        db.session.commit()
        
        flash(f'Order #{new_order.id} placed successfully!', 'success')
        return redirect(url_for('customer.order_track', order_id=new_order.id))
        
    return render_template('customer/checkout.html', 
                           items=items, 
                           subtotal=subtotal, 
                           delivery_fee=delivery_fee, 
                           tax=tax, 
                           grand_total=grand_total,
                           user_address=user_address)

@customer_bp.route('/orders')
@login_required
@customer_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/orders.html', orders=orders)

@customer_bp.route('/track/<int:order_id>')
@login_required
@customer_required
def order_track(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    statuses = ['Placed', 'Confirmed', 'Assigned', 'Accepted', 'Out for Delivery', 'Delivered']
    current_index = statuses.index(order.order_status) if order.order_status in statuses else 0
    
    return render_template('customer/track.html', order=order, statuses=statuses, current_index=current_index)

@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    user_address = Address.query.filter_by(user_id=user.id, is_default=True).first()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            user.name = request.form.get('name', user.name)
            user.phone = request.form.get('phone', user.phone)
            
            address_text = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            pincode = request.form.get('pincode')
            
            if user_address:
                user_address.address = address_text
                user_address.city = city
                user_address.state = state
                user_address.pincode = pincode
            else:
                user_address = Address(
                    user_id=user.id,
                    address=address_text,
                    city=city,
                    state=state,
                    pincode=pincode,
                    is_default=True
                )
                db.session.add(user_address)
                
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        elif action == 'change_password':
            old_pw = request.form.get('old_password')
            new_pw = request.form.get('new_password')
            confirm_pw = request.form.get('confirm_password')
            
            if not user.check_password(old_pw):
                flash('Current password is incorrect.', 'danger')
            elif new_pw != confirm_pw:
                flash('New passwords do not match.', 'danger')
            elif len(new_pw) < 6:
                flash('Password must be at least 6 characters.', 'warning')
            else:
                user.set_password(new_pw)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                
        return redirect(url_for('customer.profile'))
        
    return render_template('customer/profile.html', user=user, address=user_address)

@customer_bp.route('/download-diagrams-pdf')
def download_diagrams_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'GreenCart_Flowcharts_and_Diagrams.pdf')
    if not os.path.exists(pdf_path):
        from generate_flowcharts_pdf import draw_block_diagram
        # Trigger generator script if missing
        import subprocess
        subprocess.run(['python', 'generate_flowcharts_pdf.py'], check=False)
        
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='GreenCart_Flowcharts_and_Diagrams.pdf')
    flash('PDF document is currently generating, please refresh.', 'warning')
    return redirect(url_for('customer.index'))
