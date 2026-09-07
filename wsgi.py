import os
from app import create_app, db
from seed_data import seed_database

app = create_app()

with app.app_context():
    db.create_all()
    from app.models import User
    if User.query.count() == 0:
        print("Initializing & Seeding GreenCart Database for Production...")
        seed_database()

if __name__ == '__main__':
    app.run()
