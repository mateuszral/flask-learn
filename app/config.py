from datetime import timedelta

class Config:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    UPLOAD_FOLDER = 'static/uploads'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False