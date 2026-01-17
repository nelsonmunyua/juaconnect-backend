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
            password_hash=generate_password_hash("password123"),
            bio="Experienced plumber with 10+ years of experience in residential and commercial plumbing. Specializing in leak detection and pipe installation.",
            profile_picture="https://example.com/profiles/john.jpg",
            phone="+254712345678",
            location="Nairobi, Kenya",
            skills="Plumbing, Pipe Installation, Leak Detection, Water Heater Repair",
            experience_years=12,
            business_name="John's Quality Plumbing",
            business_address="123 Pipeline Road, Industrial Area, Nairobi",
            tax_id="A123456789X",
            hourly_rate=2500.00
        )

        artisan2 = User(
            name="Mary Artisan",
            email="mary@artisan.com",
            role="artisan",
            password_hash=generate_password_hash("password123"),
            bio="Licensed electrician specializing in residential wiring, panel upgrades, and smart home installations. Certified and insured.",
            profile_picture="https://example.com/profiles/mary.jpg",
            phone="+254723456789",
            location="Mombasa, Kenya",
            skills="Electrical Wiring, Panel Installation, Smart Home Setup, Troubleshooting",
            experience_years=8,
            business_name="Spark Electric",
            business_address="456 Current Street, Mombasa",
            tax_id="B987654321Y",
            hourly_rate=3000.00
        )

        client1 = User(
            name="Alice Client",
            email="alice@client.com",
            role="client",
            password_hash=generate_password_hash("password123"),
            bio="Homeowner looking for reliable artisans for home improvement projects.",
            profile_picture="https://example.com/profiles/alice.jpg",
            phone="+254734567890",
            location="Westlands, Nairobi",
            skills=None,  # Clients don't typically have skills
            experience_years=None,
            business_name=None,
            business_address=None,
            tax_id=None,
            hourly_rate=None
        )

        client2 = User(
            name="Bob Client",
            email="bob@client.com",
            role="client",
            password_hash=generate_password_hash("password123"),
            bio="Property manager seeking professional artisans for multiple rental properties.",
            profile_picture="https://example.com/profiles/bob.jpg",
            phone="+254745678901",
            location="Karen, Nairobi",
            skills=None,
            experience_years=None,
            business_name="Bob's Property Management",
            business_address="78 Garden Estate, Karen",
            tax_id="C123789456Z",  # Some clients might be businesses
            hourly_rate=None
        )

        # Add a third artisan for more variety
        artisan3 = User(
            name="Paul Carpenter",
            email="paul@artisan.com",
            role="artisan",
            password_hash=generate_password_hash("password123"),
            bio="Master carpenter specializing in custom furniture and home renovations.",
            profile_picture="https://example.com/profiles/paul.jpg",
            phone="+254756789012",
            location="Nakuru, Kenya",
            skills="Carpentry, Furniture Making, Cabinetry, Wood Finishing",
            experience_years=15,
            business_name="Paul's Fine Woodworks",
            business_address="89 Timber Lane, Nakuru",
            tax_id="D456123789W",
            hourly_rate=2000.00
        )

        db.session.add_all([artisan1, artisan2, artisan3, client1, client2])
        db.session.commit()

        print("🛠 Creating services...")

        # -------- SERVICES --------
        service1 = Service(
            title="Emergency Leak Repair",
            description="24/7 emergency plumbing service for leaks and burst pipes",
            price=3000,
            category="Plumbing",
            duration=120,
            artisan_id=artisan1.id
        )

        service2 = Service(
            title="Complete House Rewiring",
            description="Full electrical rewiring including safety upgrades and new panels",
            price=5000,
            category="Electrical",
            duration=180,
            artisan_id=artisan2.id
        )

        service3 = Service(
            title="Custom Kitchen Cabinets",
            description="Design and installation of custom kitchen cabinets and storage",
            price=15000,
            category="Carpentry",
            duration=480,
            artisan_id=artisan3.id
        )

        service4 = Service(
            title="Bathroom Renovation",
            description="Complete bathroom remodeling including fixtures and tiling",
            price=12000,
            category="Renovation",
            duration=360,
            artisan_id=artisan1.id
        )

        service5 = Service(
            title="Smart Home Installation",
            description="Installation of smart lighting, security, and automation systems",
            price=8000,
            category="Electrical",
            duration=240,
            artisan_id=artisan2.id
        )

        service6 = Service(
            title="Custom Dining Table",
            description="Handcrafted dining table made from reclaimed wood",
            price=25000,
            category="Furniture",
            duration=600,
            artisan_id=artisan3.id
        )

        db.session.add_all([service1, service2, service3, service4, service5, service6])
        db.session.commit()

        print("📅 Creating bookings...")

        # -------- BOOKINGS --------
        booking1 = Booking(
            date=datetime.utcnow() + timedelta(days=2),
            status="confirmed",
            notes="Please arrive early. House is the blue one with white trim.",
            client_id=client1.id,
            service_id=service1.id
        )

        booking2 = Booking(
            date=datetime.utcnow() + timedelta(days=5),
            status="pending",
            notes="Need urgent service - flickering lights throughout the house.",
            client_id=client2.id,
            service_id=service2.id
        )

        booking3 = Booking(
            date=datetime.utcnow() + timedelta(days=7),
            status="completed",
            notes="Installation completed on time. Very satisfied.",
            client_id=client1.id,
            service_id=service5.id
        )

        booking4 = Booking(
            date=datetime.utcnow() + timedelta(days=10),
            status="confirmed",
            notes="Custom measurements provided. Please confirm before starting.",
            client_id=client2.id,
            service_id=service6.id
        )

        db.session.add_all([booking1, booking2, booking3, booking4])
        db.session.commit()

        print("⭐ Creating reviews...")

        # -------- REVIEWS --------
        review1 = Review(
            rating=5,
            comment="John arrived on time and fixed the leak quickly. Very professional and knowledgeable!",
            client_id=client1.id,
            artisan_id=artisan1.id,
            helpful_count=5
        )

        review2 = Review(
            rating=4,
            comment="Mary did a great job with the wiring. Minor delay but work was excellent.",
            client_id=client2.id,
            artisan_id=artisan2.id,
            helpful_count=3
        )

        review3 = Review(
            rating=5,
            comment="Paul's craftsmanship is exceptional! The dining table is exactly what we wanted.",
            client_id=client1.id,
            artisan_id=artisan3.id,
            helpful_count=7
        )

        review4 = Review(
            rating=5,
            comment="Outstanding electrical work. Our smart home system works perfectly!",
            client_id=client2.id,
            artisan_id=artisan2.id,
            helpful_count=2
        )

        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()

        print("🔗 Linking reviews to services...")

        # -------- SERVICE_REVIEWS (M2M) --------
        review1.services.append(service1)
        review2.services.append(service2)
        review3.services.append(service6)
        review4.services.append(service5)

        db.session.commit()

        print("✅ Database seeded successfully!")
        print("\n📊 Seeding Summary:")
        print(f"   Users: {User.query.count()} (Artisans: {User.query.filter_by(role='artisan').count()}, Clients: {User.query.filter_by(role='client').count()})")
        print(f"   Services: {Service.query.count()}")
        print(f"   Bookings: {Booking.query.count()}")
        print(f"   Reviews: {Review.query.count()}")


if __name__ == "__main__":
    seed_data()