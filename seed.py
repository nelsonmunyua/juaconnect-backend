from app import app
from models import (
    db,
    User,
    ArtisanProfile,
    ClientProfile,
    Skill,
    ArtisanSkill,
    ServiceRequest,
    Booking,
    Payment,
    Review
)
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():

        print("🌱 Clearing database...")
        db.drop_all()
        db.create_all()

        # --------------------
        # USERS
        # --------------------
        print("👤 Creating users...")

        client_user = User(
            full_name="John Kamau",
            phone_number="0712345678",
            email="john@example.com",
            password="hashed_password",
            role="client",
            is_verified=True
        )

        artisan_user = User(
            full_name="Peter Mwangi",
            phone_number="0798765432",
            email="peter@example.com",
            password="hashed_password",
            role="artisan",
            is_verified=True
        )

        db.session.add_all([client_user, artisan_user])
        db.session.commit()

        # --------------------
        # PROFILES
        # --------------------
        client_profile = ClientProfile(
            user_id=client_user.id,
            location="Nairobi"
        )

        artisan_profile = ArtisanProfile(
            user_id=artisan_user.id,
            bio="Experienced plumber and handyman",
            location="Nairobi",
            hourly_rate=800,
            years_of_experience=5
        )

        db.session.add_all([client_profile, artisan_profile])
        db.session.commit()

        # --------------------
        # SKILLS
        # --------------------
        print("🛠 Creating skills...")

        skills = [
            Skill(name="Plumbing", description="Water systems & repairs"),
            Skill(name="Electrical", description="Wiring & installations"),
            Skill(name="Carpentry", description="Woodwork & furniture")
        ]

        db.session.add_all(skills)
        db.session.commit()

        # --------------------
        # ASSIGN SKILLS TO ARTISAN
        # --------------------
        artisan_skills = [
            ArtisanSkill(artisan_id=artisan_profile.id, skill_id=skills[0].id),
            ArtisanSkill(artisan_id=artisan_profile.id, skill_id=skills[1].id)
        ]

        db.session.add_all(artisan_skills)
        db.session.commit()

        # --------------------
        # SERVICE REQUEST
        # --------------------
        print("📋 Creating service request...")

        service_request = ServiceRequest(
            client_id=client_profile.id,
            skill_id=skills[0].id,
            description="Fix leaking sink",
            location="Westlands",
            preferred_date=datetime.now() + timedelta(days=2),
            budget=3000
        )

        db.session.add(service_request)
        db.session.commit()

        # --------------------
        # BOOKING
        # --------------------
        booking = Booking(
            service_request_id=service_request.id,
            artisan_id=artisan_profile.id,
            scheduled_date=datetime.now() + timedelta(days=3),
            agreed_price=2800
        )

        db.session.add(booking)
        db.session.commit()

        # --------------------
        # PAYMENT
        # --------------------
        payment = Payment(
            booking_id=booking.id,
            amount=2800,
            payment_method="mpesa",
            payment_status="paid"
        )

        db.session.add(payment)
        db.session.commit()

        # --------------------
        # REVIEW
        # --------------------
        review = Review(
            booking_id=booking.id,
            client_id=client_profile.id,
            artisan_id=artisan_profile.id,
            rating=5,
            comment="Great work, very professional!"
        )

        db.session.add(review)
        db.session.commit()

        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
