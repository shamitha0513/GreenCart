from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Order, DeliveryPartner, User
from app.utils import delivery_required

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/dashboard')
@login_required
@delivery_required
def dashboard():
    assigned_orders = Order.query.filter_by(delivery_partner_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    assigned_count = sum(1 for o in assigned_orders if o.order_status in ['Assigned', 'Accepted'])
    pending_count = sum(1 for o in assigned_orders if o.order_status == 'Assigned')
    out_for_delivery_count = sum(1 for o in assigned_orders if o.order_status == 'Out for Delivery')
    completed_count = sum(1 for o in assigned_orders if o.order_status == 'Delivered')
    
    dp_profile = DeliveryPartner.query.filter_by(user_id=current_user.id).first()
    
    return render_template('delivery/dashboard.html',
                           orders=assigned_orders,
                           assigned_count=assigned_count,
                           pending_count=pending_count,
                           out_for_delivery_count=out_for_delivery_count,
                           completed_count=completed_count,
                           profile=dp_profile)

@delivery_bp.route('/update-status/<int:order_id>', methods=['POST'])
@login_required
@delivery_required
def update_status(order_id):
    order = Order.query.filter_by(id=order_id, delivery_partner_id=current_user.id).first_or_404()
    new_status = request.form.get('status')
    
    # State machine transition rules from PDF (Section 50)
    valid_transitions = {
        'Assigned': ['Accepted'],
        'Accepted': ['Out for Delivery'],
        'Out for Delivery': ['Delivered']
    }
    
    if new_status in valid_transitions.get(order.order_status, []):
        order.order_status = new_status
        if new_status == 'Delivered' and order.payment:
            order.payment_status = 'Successful'
            order.payment.payment_status = 'Successful'
            
        db.session.commit()
        flash(f'Order #{order.id} status updated to "{new_status}".', 'success')
    else:
        flash(f'Invalid status transition from {order.order_status} to {new_status}.', 'warning')
        
    return redirect(url_for('delivery.dashboard'))

@delivery_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@delivery_required
def profile():
    dp_profile = DeliveryPartner.query.filter_by(user_id=current_user.id).first()
    if not dp_profile:
        dp_profile = DeliveryPartner(user_id=current_user.id)
        db.session.add(dp_profile)
        
    if request.method == 'POST':
        dp_profile.availability_status = request.form.get('availability_status', 'Available')
        dp_profile.vehicle_type = request.form.get('vehicle_type', 'Two Wheeler')
        current_user.phone = request.form.get('phone', current_user.phone)
        db.session.commit()
        flash('Delivery profile updated successfully.', 'success')
        return redirect(url_for('delivery.profile'))
        
    return render_template('delivery/profile.html', profile=dp_profile)
