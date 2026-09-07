from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='CUSTOMER') # ADMIN, CUSTOMER, DELIVERY_PARTNER
    status = db.Column(db.String(20), default='ACTIVE') # ACTIVE, INACTIVE, BLOCKED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', foreign_keys='Order.user_id', backref='customer', lazy=True)
    cart = db.relationship('Cart', backref='user', uselist=False, cascade='all, delete-orphan')
    delivery_profile = db.relationship('DeliveryPartner', backref='user', uselist=False, cascade='all, delete-orphan')
    service_bookings = db.relationship('ServiceBooking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'ADMIN'
        
    def is_customer(self):
        return self.role == 'CUSTOMER'

    def is_delivery_partner(self):
        return self.role == 'DELIVERY_PARTNER'


class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    is_default = db.Column(db.Boolean, default=True)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    
    plants = db.relationship('Plant', backref='category', lazy=True)


class Plant(db.Model):
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False, index=True)
    scientific_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=True)
    care_instructions = db.Column(db.Text, nullable=True)
    sunlight = db.Column(db.String(100), nullable=True) # Full Sun, Partial Shade, Low Light
    water_requirement = db.Column(db.String(100), nullable=True) # Daily, Weekly, Bi-weekly
    soil_type = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=True) # Small, Medium, Large
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0) # Percentage e.g. 10.0
    stock_quantity = db.Column(db.Integer, nullable=False, default=10)
    image = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='ACTIVE') # ACTIVE, OUT_OF_STOCK, INACTIVE
    rating = db.Column(db.Float, default=4.5)
    reviews_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def final_price(self):
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100.0), 2)
        return self.price

    @property
    def stock_status(self):
        if self.stock_quantity <= 0:
            return 'Out of Stock'
        elif self.stock_quantity <= 5:
            return 'Low Stock'
        return 'In Stock'


class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    
    plant = db.relationship('Plant')


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    delivery_fee = db.Column(db.Float, default=49.0)
    tax_amount = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending') # Pending, Successful, Failed, Refunded, COD
    order_status = db.Column(db.String(30), default='Placed') # Placed, Confirmed, Assigned, Accepted, Out for Delivery, Delivered, Cancelled
    delivery_partner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    delivery_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    delivery_partner = db.relationship('User', foreign_keys=[delivery_partner_id], backref='assigned_orders')


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    plant_name = db.Column(db.String(150), nullable=False)
    plant_image = db.Column(db.String(255), nullable=True)
    
    plant = db.relationship('Plant')


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False) # UPI, Credit/Debit Card, Cash on Delivery
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_status = db.Column(db.String(20), default='Pending') # Pending, Successful, Failed, Refunded
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)


class DeliveryPartner(db.Model):
    __tablename__ = 'delivery_partners'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    availability_status = db.Column(db.String(20), default='Available') # Available, Busy, Offline
    current_status = db.Column(db.String(100), default='Ready for deliveries')
    vehicle_type = db.Column(db.String(50), default='Two Wheeler')


class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='ACTIVE')


class ServiceBooking(db.Model):
    __tablename__ = 'service_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service = db.relationship('Service', backref='bookings')


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
