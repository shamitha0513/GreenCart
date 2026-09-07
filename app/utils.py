import os
import re
import csv
import io
from functools import wraps
from flask import redirect, url_for, flash, abort, Response, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access the admin area.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('Access denied. Administrator privileges required.', 'danger')
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_customer():
            flash('Access denied. Customer account required.', 'danger')
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def delivery_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access the delivery partner panel.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_delivery_partner():
            flash('Access denied. Delivery Partner account required.', 'danger')
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    # 10 digit or international phone validation
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return len(cleaned) >= 10 and cleaned.isdigit()

def validate_password_strength(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def save_uploaded_image(file_storage, folder_name='plants'):
    if not file_storage or file_storage.filename == '':
        return None
    
    filename = secure_filename(file_storage.filename)
    # prepend timestamp to prevent name collision
    import time
    unique_filename = f"{int(time.time())}_{filename}"
    
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
    os.makedirs(target_dir, exist_ok=True)
    
    filepath = os.path.join(target_dir, unique_filename)
    file_storage.save(filepath)
    return f"images/plants/{unique_filename}"

def generate_csv_response(headers, rows, filename="report.csv"):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
        
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
