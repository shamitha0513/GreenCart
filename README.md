# GreenCart - Online Plant Shopping & Plant Services Platform

GreenCart is a production-ready, full-stack, database-driven web application built with **Python (Flask)**, **SQLAlchemy**, **HTML5/CSS3**, **Bootstrap 5**, and **Chart.js**.

The platform supports 3 user roles: **Customer**, **Admin**, and **Delivery Partner**, operating under a single common login portal with role-based redirection, live order status tracking, stock automation, payment reports, and 180+ plants across 12 categories.

---

## Key Features

1. **Role-Based Authentication & Common Login**: Single `/login` page automatically routes:
   - `ADMIN` → Admin Management Dashboard (`/admin/dashboard`)
   - `CUSTOMER` → Customer Dashboard (`/dashboard`)
   - `DELIVERY_PARTNER` → Delivery Partner Dashboard (`/delivery/dashboard`)
2. **180+ Plants Catalog**: 12 distinct categories with 15 realistic plant species each, including care guidelines, scientific names, stock levels, and accurate images.
3. **Gift Suggestions & Plant Services**: Occasion-based plant gifts and interactive booking form for plant health, repotting, and garden setup services.
4. **Stock Automation**: Stock is automatically deducted upon successful checkout and restored upon order cancellation.
5. **Live Order Tracking (AJAX Polling)**: Real-time progress tracker (`Placed` → `Confirmed` → `Assigned` → `Accepted` → `Out for Delivery` → `Delivered`).
6. **Admin Dashboard & Analytics**: Interactive Chart.js graphs for revenue, category sales, order status distribution, top selling plants, low stock alerts, and CSV payment report export.
7. **Delivery Partner Workflow**: Interactive state machine buttons to accept orders, mark out for delivery, and complete delivery.
8. **Light/Dark Mode**: Global theme switcher with local storage persistence.

---

## Demo Accounts

The system automatically populates the following accounts when initialized via `python seed_data.py`:

| Role | Username | Email | Password |
|---|---|---|---|
| **Admin** | `admin` | `admin@greencart.com` | `admin123` |
| **Customer** | `customer1` | `john@example.com` | `cust123` |
| **Delivery Partner** | `delivery1` | `alex@greencart.com` | `del123` |

---

## Setup & Local Execution Guide

### Prerequisites
- Python 3.9+
- pip (Python package installer)

### Step 1: Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database & Environment Configuration
The application is pre-configured with **SQLite** out-of-the-box for zero-setup execution.

To use **MySQL** (optional):
1. Create a MySQL database named `greencart_db`.
2. Copy `.env.example` to `.env` and set your connection string:
```ini
DATABASE_URL=mysql+pymysql://username:password@localhost/greencart_db
```

### Step 4: Seed Database
Populate 180+ plants, 12 categories, services, accurate images, and demo accounts:
```bash
python seed_data.py
```

### Step 5: Run Application
```bash
python run.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Testing End-to-End Workflow

1. **Customer Workflow**:
   - Login as `customer1` / `cust123`.
   - Browse catalog at `/plants`, select a plant, view care details, click **Add to Cart**.
   - Proceed to `/checkout`, select UPI or Card payment, and place order.
   - You will be redirected to live order tracking (`/track/<order_id>`).

2. **Admin Workflow**:
   - Open a new private window and login as `admin` / `admin123`.
   - On the Admin Dashboard, observe revenue metrics, low stock alerts, and Chart.js graphs.
   - Go to **Orders**, click **Confirm Order**, then click **Assign Partner** and choose `Alex Swift (Delivery Partner)`.

3. **Delivery Partner Workflow**:
   - Open another window and login as `delivery1` / `del123`.
   - In the Delivery Dashboard, view assigned order.
   - Click **1. Accept Order**, then click **2. Start Delivery (Out for Delivery)**, and finally click **3. Mark as Delivered**.

4. **Verify Live Updates**:
   - Observe the Customer's tracking page update in real-time to **Delivered** via AJAX polling without refreshing!

---

## Production Deployment Checklist

1. Set `FLASK_ENV=production` and generate a strong random `SECRET_KEY` in `.env`.
2. Use WSGI server such as Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn "app:create_app()" -w 4 -b 0.0.0.0:8000
   ```
3. Configure Nginx reverse proxy with SSL certificate (Certbot).
4. Connect to MySQL / PostgreSQL database with secure credentials.
