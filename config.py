import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///moviebooking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    MAX_TICKETS_PER_ORDER = 10
    THEATERS = ['Lubbock', 'Amarillo', 'Levelland', 'Plainview', 'Snyder', 'Abilene']
    SHOWTIMES = ['2:00 PM', '5:00 PM', '8:00 PM', '10:00 PM']
    PAYMENT_METHODS = ['credit', 'paypal', 'venmo']    