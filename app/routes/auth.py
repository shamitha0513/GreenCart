from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Address, Cart, DeliveryPartner
from app.utils import validate_email, validate_phone, validate_password_strength

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_delivery_partner():
            return redirect(url_for('delivery.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
            
    if request.method == 'POST':
        login_input = request.form.get('login_input', '').strip()
        password = request.form.get('password', '')
        
        if not login_input or not password:
            flash('Please enter both email/username and password.', 'warning')
            return render_template('auth/login.html')
            
        # Search by email or username
        user = User.query.filter(
            (User.email == login_input) | (User.username == login_input)
        ).first()
        
        if user and user.check_password(password):
            if user.status != 'ACTIVE':
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return render_template('auth/login.html')
                
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Role-based redirection rule from PDF
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_delivery_partner():
                return redirect(url_for('delivery.dashboard'))
            else:
                return redirect(url_for('customer.dashboard'))
        else:
            flash('Invalid username/email or password.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        pincode = request.form.get('pincode', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'CUSTOMER').upper()
        
        # Security rule from PDF: Admin registration must NOT be publicly available
        if role not in ['CUSTOMER', 'DELIVERY_PARTNER']:
            role = 'CUSTOMER'
            
        # Validations
        if not all([name, email, phone, address, city, state, pincode, username, password, confirm_password]):
            flash('All fields are required.', 'warning')
            return render_template('auth/register.html')
            
        if not validate_email(email):
            flash('Please enter a valid email address.', 'warning')
            return render_template('auth/register.html')
            
        if not validate_phone(phone):
            flash('Please enter a valid phone number (at least 10 digits).', 'warning')
            return render_template('auth/register.html')
            
        is_valid_pw, msg = validate_password_strength(password)
        if not is_valid_pw:
            flash(msg, 'warning')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'warning')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email address is already registered.', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username is already taken.', 'danger')
            return render_template('auth/register.html')
            
        # Create user
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            username=username,
            role=role,
            status='ACTIVE'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush() # get user id
        
        # Create default address
        new_address = Address(
            user_id=new_user.id,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            is_default=True
        )
        db.session.add(new_address)
        
        # Initialize Cart for Customer
        if role == 'CUSTOMER':
            new_cart = Cart(user_id=new_user.id)
            db.session.add(new_cart)
            
        # Initialize Delivery Partner profile
        if role == 'DELIVERY_PARTNER':
            new_dp = DeliveryPartner(
                user_id=new_user.id,
                availability_status='Available',
                current_status='Ready for deliveries',
                vehicle_type='Two Wheeler'
            )
            db.session.add(new_dp)
            
        db.session.commit()
        
        flash('Registration successful. Please login to continue.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
