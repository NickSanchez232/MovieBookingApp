from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    synopsis = db.Column(db.Text)
    cast = db.Column(db.String(500))
    director = db.Column(db.String(200))
    runtime = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    is_upcoming = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300))
    trailer_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='movie', lazy=True)
    reviews = db.relationship('Review', backref='movie', lazy=True, cascade='all, delete-orphan')
    
    def get_embed_trailer_url(self):
        """Converts a standard YouTube URL to an embed URL."""
        if self.trailer_url and 'v=' in self.trailer_url:
            video_id = self.trailer_url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    def __repr__(self):
        return f'<Movie {self.title}>'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    theater = db.Column(db.String(100), nullable=False)
    showtime = db.Column(db.String(50), nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='unused')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_order_number():
        return str(uuid.uuid4())[:8].upper()
    
    def can_refund(self):
        from datetime import timedelta
        if self.status != 'unused':
            return False
        show_datetime = datetime.combine(self.show_date, datetime.min.time())
        time_until_show = show_datetime - datetime.utcnow()
        return time_until_show.total_seconds() > 86400
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id} - Movie {self.movie_id}>'