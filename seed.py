from app import app
from models import db, User, Service, Booking, Review
from datetime import datetime, timedelta

with app.app_context():
    # Clear existing data
    Review.query.delete()
    Booking.query.delete()
    Service.query.delete()
    User.query.delete()
    
    # Create users
    artisan1 = User(username='john_carpenter', email='john@example.com', is_artisan=True)
    artisan2 = User(username='sarah_designer', email='sarah@example.com', is_artisan=True)
    client1 = User(username='client_mike', email='mike@example.com', is_artisan=False)
    client2 = User(username='client_anna', email='anna@example.com', is_artisan=False)
    
    db.session.add_all([artisan1, artisan2, client1, client2])
    db.session.commit()
    
    # Create services
    service1 = Service(
        title='Custom Furniture Making',
        description='Handcrafted wooden furniture',
        price=500.00,
        category='Carpentry',
        duration=300,
        artisan_id=artisan1.id
    )
    
    service2 = Service(
        title='Interior Design Consultation',
        description='Home interior planning and design',
        price=150.00,
        category='Design',
        duration=120,
        artisan_id=artisan2.id
    )
    
    service3 = Service(
        title='Cabinet Installation',
        description='Kitchen and bathroom cabinet fitting',
        price=300.00,
        category='Carpentry',
        duration=240,
        artisan_id=artisan1.id
    )
    
    db.session.add_all([service1, service2, service3])
    db.session.commit()
    
    # Create bookings
    booking1 = Booking(
        date=datetime.utcnow() + timedelta(days=7),
        status='confirmed',
        client_id=client1.id,
        service_id=service1.id
    )
    
    booking2 = Booking(
        date=datetime.utcnow() + timedelta(days=14),
        status='pending',
        client_id=client2.id,
        service_id=service2.id
    )
    
    db.session.add_all([booking1, booking2])
    db.session.commit()
    
    # Create reviews (many-to-many)
    review1 = Review(
        rating=5,
        comment='Excellent work! Highly recommended.',
        client_id=client1.id,
        artisan_id=artisan1.id,
        helpful_count=3
    )
    
    review2 = Review(
        rating=4,
        comment='Good service, timely completion.',
        client_id=client2.id,
        artisan_id=artisan2.id,
        helpful_count=1
    )
    
    # Associate reviews with services
    review1.services.append(service1)
    review2.services.append(service2)
    
    db.session.add_all([review1, review2])
    db.session.commit()
    
    print("Database seeded successfully!")