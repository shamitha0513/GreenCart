import os
from app import create_app, db
from seed_data import seed_database

app = create_app()

with app.app_context():
    db.create_all()
    print("Syncing GreenCart Database and Plant Image mappings...")
    try:
        seed_database()
    except Exception as e:
        print(f"Database seed sync warning: {e}")

if __name__ == '__main__':
    app.run()
