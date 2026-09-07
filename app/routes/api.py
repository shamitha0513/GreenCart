from flask import Blueprint, jsonify
from flask_login import current_user
from app.models import Order, Plant, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/order-status/<int:order_id>')
def order_status(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
        
    partner_name = order.delivery_partner.name if order.delivery_partner else "Not Assigned"
    partner_phone = order.delivery_partner.phone if order.delivery_partner else ""
    
    return jsonify({
        'id': order.id,
        'order_status': order.order_status,
        'payment_status': order.payment_status,
        'delivery_partner': partner_name,
        'delivery_partner_phone': partner_phone,
        'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@api_bp.route('/live-summary')
def live_summary():
    if not current_user.is_authenticated:
        return jsonify({})
        
    if current_user.is_admin():
        pending_orders = Order.query.filter(Order.order_status.in_(['Placed', 'Confirmed', 'Assigned', 'Accepted', 'Out for Delivery'])).count()
        low_stock_count = Plant.query.filter(Plant.stock_quantity <= 5).count()
        return jsonify({
            'role': 'ADMIN',
            'pending_orders': pending_orders,
            'low_stock_count': low_stock_count
        })
    elif current_user.is_delivery_partner():
        assigned = Order.query.filter_by(delivery_partner_id=current_user.id, order_status='Assigned').count()
        active = Order.query.filter(Order.delivery_partner_id == current_user.id, Order.order_status.in_(['Accepted', 'Out for Delivery'])).count()
        return jsonify({
            'role': 'DELIVERY_PARTNER',
            'assigned': assigned,
            'active': active
        })
    else:
        active_orders = Order.query.filter(Order.user_id == current_user.id, Order.order_status != 'Delivered', Order.order_status != 'Cancelled').all()
        return jsonify({
            'role': 'CUSTOMER',
            'active_orders': [{'id': o.id, 'status': o.order_status} for o in active_orders]
        })
