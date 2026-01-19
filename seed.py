from app import app, db, User, Service, Booking, Review
from datetime import datetime, timedelta

def seed_database():
    print("🌱 Seeding database...")
    
    # Clear existing data
    db.session.query(Review).delete()
    db.session.query(Booking).delete()
    db.session.query(Service).delete()
    db.session.query(User).delete()
    
    # Create users
    users = [
        User(username='john_carpenter', email='john@example.com', is_artisan=True, bio='Master carpenter with 15 years experience'),
        User(username='sarah_designer', email='sarah@example.com', is_artisan=True, bio='Interior designer specializing in modern homes'),
        User(username='client_mike', email='mike@example.com', is_artisan=False, bio='Homeowner looking for quality services'),
        User(username='client_anna', email='anna@example.com', is_artisan=False, bio='Small business owner'),
    ]
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    
    # Create services
    services = [
        Service(
            title='Custom Furniture Making',
            description='Handcrafted wooden furniture tailored to your needs',
            price=500.00,
            category='Carpentry',
            duration=300,
            artisan_id=1,
            is_published=True
        ),
        Service(
            title='Interior Design Consultation',
            description='Home interior planning and design services',
            price=150.00,
            category='Design',
            duration=120,
            artisan_id=2,
            is_published=True
        ),
        Service(
            title='Cabinet Installation',
            description='Kitchen and bathroom cabinet fitting',
            price=300.00,
            category='Carpentry',
            duration=240,
            artisan_id=1,
            is_published=True
        ),
        Service(
            title='Plumbing Repair',
            description='Fix leaks and pipe installations',
            price=200.00,
            category='Plumbing',
            duration=180,
            artisan_id=1,
            is_published=True
        ),
    ]
    
    for service in services:
        db.session.add(service)
    
    db.session.commit()
    print(f"✅ Created {len(services)} services")
    
    # Create bookings
    bookings = [
        Booking(
            date=datetime.utcnow() + timedelta(days=7),
            status='confirmed',
            client_id=3,
            service_id=1
        ),
        Booking(
            date=datetime.utcnow() + timedelta(days=14),
            status='pending',
            client_id=4,
            service_id=2
        ),
        Booking(
            date=datetime.utcnow() + timedelta(days=10),
            status='completed',
            client_id=3,
            service_id=3
        ),
    ]
    
    for booking in bookings:
        db.session.add(booking)
    
    db.session.commit()
    print(f"✅ Created {len(bookings)} bookings")
    
    # Create reviews
    reviews = [
        Review(
            rating=5,
            comment='Excellent work! Highly recommended.',
            client_id=3,
            artisan_id=1,
            helpful_count=3
        ),
        Review(
            rating=4,
            comment='Good service, timely completion.',
            client_id=4,
            artisan_id=2,
            helpful_count=1
        ),
        Review(
            rating=5,
            comment='Perfect cabinet installation, very professional.',
            client_id=3,
            artisan_id=1,
            helpful_count=2
        ),
    ]
    
    for review in reviews:
        db.session.add(review)
    
    db.session.commit()
    print(f"✅ Created {len(reviews)} reviews")
    
    print("🎉 Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()