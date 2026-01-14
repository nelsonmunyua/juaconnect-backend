from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

# Many-to-Many association table for Reviews
service_reviews = db.Table('service_reviews',
    db.Column('review_id', db.Integer, db.ForeignKey('reviews.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.Enum("client", "artisan"), default="client")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # One-to-Many: Artisan has many services
    services = db.relationship('Service', backref='artisan', lazy=True)
    
    # One-to-Many: Client has many bookings
    bookings = db.relationship('Booking', backref='client', lazy=True, foreign_keys='Booking.client_id')
    
    # Many-to-Many: Users can receive reviews
    reviews_received = db.relationship('Review', backref='artisan', lazy=True, foreign_keys='Review.artisan_id')
    
    # serialize_rules = ('-password_hash', '-services.artisan', '-bookings.client', '-reviews_received.artisan')
    
    serialize_rules = (
    '-services',
    '-bookings',
    '-reviews_received',
    '-reviews_written'
    )
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email format")
        return email
    
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        return username

class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # in minutes
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())    
    # Foreign Keys
    artisan_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # One-to-Many: Service has many bookings
    bookings = db.relationship('Booking', backref='service', lazy=True)
    
    # Many-to-Many: Services can have reviews
    reviews = db.relationship('Review', secondary=service_reviews, lazy='subquery',
                            backref=db.backref('services', lazy=True))
    
    # serialize_rules = ('-artisan.services', '-bookings.service', '-reviews.services')
    serialize_rules = (
    '-artisan',
    '-bookings',
    '-reviews'
    )
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    serialize_rules = ('-client.bookings', '-service.bookings')

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at =db.Column(db.DataTime, onupdate=db.func.now())
    
    # Foreign Keys (Many-to-Many relationship through Review)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artisan_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # User-submittable attribute for many-to-many
    helpful_count = db.Column(db.Integer, default=0)  # Users can mark review as helpful
    
    # serialize_rules = ('-client.reviews_received', '-artisan.reviews_received')
    serialize_rules = (
    '-artisan',
    '-client',
    '-services'
   )
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating