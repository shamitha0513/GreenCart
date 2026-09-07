import os
from app import create_app, db
from seed_data import seed_database

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure database tables exist and seed demo data if empty
        db.create_all()
        from app.models import User
        if User.query.count() == 0:
            print("Database empty. Auto-seeding initial plant catalog and accounts...")
            seed_database()

    print("Starting GreenCart Web Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
