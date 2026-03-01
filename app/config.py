import os

from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    UPLOAD_FOLDER = 'static/uploads'
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False