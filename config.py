import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'greencart_secret_key_super_secure_2026_change_in_production')
    
    # SQLite default fallback if MySQL is not configured
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "greencart.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'images', 'plants')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    
    # Pagination & Cache Settings
    PLANTS_PER_PAGE = 12
    TEMPLATES_AUTO_RELOAD = True
