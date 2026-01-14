from app import app
from models import db, User, Service, Booking, Review
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

def seed_data():
    with app.app_context():
        print("🌱 Clearing existing data...")

        Review.query.delete()
        Booking.query.delete()
        Service.query.delete()
        User.query.delete()

        db.session.commit()

        print("👤 Creating users...")

        # -------- USERS --------
        artisan1 = User(
            name="John Artisan",
            email="john@artisan.com",
            role="artisan",
            password_hash=generate_password_hash("password123")
        )

        artisan2 = User(
            name="Mary Artisan",
            email="mary@artisan.com",
            role="artisan",
            password_hash=generate_password_hash("password123")
        )

        client1 = User(
            name="Alice Client",
            email="alice@client.com",
            role="client",
            password_hash=generate_password_hash("password123")
        )

        client2 = User(
            name="Bob Client",
            email="bob@client.com",
            role="client",
            password_hash=generate_password_hash("password123")
        )

        db.session.add_all([artisan1, artisan2, client1, client2])
        db.session.commit()

        print("🛠 Creating services...")

        # -------- SERVICES --------
        service1 = Service(
            title="House Plumbing",
            description="Fixing leaks and pipe installation",
            price=3000,
            category="Plumbing",
            duration=120,
            artisan_id=artisan1.id
        )

        service2 = Service(
            title="Electrical Wiring",
            description="Full house wiring and repairs",
            price=5000,
            category="Electrical",
            duration=180,
            artisan_id=artisan2.id
        )

        service3 = Service(
            title="Bathroom Renovation",
            description="Complete bathroom remodeling",
            price=15000,
            category="Renovation",
            duration=480,
            artisan_id=artisan1.id
        )

        db.session.add_all([service1, service2, service3])
        db.session.commit()

        print("📅 Creating bookings...")

        # -------- BOOKINGS --------
        booking1 = Booking(
            date=datetime.utcnow() + timedelta(days=2),
            status="confirmed",
            notes="Please arrive early",
            client_id=client1.id,
            service_id=service1.id
        )

        booking2 = Booking(
            date=datetime.utcnow() + timedelta(days=5),
            status="pending",
            notes="Need urgent service",
            client_id=client2.id,
            service_id=service2.id
        )

        db.session.add_all([booking1, booking2])
        db.session.commit()

        print("⭐ Creating reviews...")

        # -------- REVIEWS --------
        review1 = Review(
            rating=5,
            comment="Excellent work! Very professional.",
            client_id=client1.id,
            artisan_id=artisan1.id,
            helpful_count=3
        )

        review2 = Review(
            rating=4,
            comment="Good job, but arrived a bit late.",
            client_id=client2.id,
            artisan_id=artisan2.id,
            helpful_count=1
        )

        db.session.add_all([review1, review2])
        db.session.commit()

        print("🔗 Linking reviews to services...")

        # -------- SERVICE_REVIEWS (M2M) --------
        review1.services.append(service1)
        review2.services.append(service2)

        db.session.commit()

        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
