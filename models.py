from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

# Naming convention (same pattern you used)
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


# --------------------
# USER
# --------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.Text(), nullable=False)
    phone_number = db.Column(db.Text(), nullable=False, unique=True)
    email = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text())
    role = db.Column(
        db.Enum("client", "artisan", "admin"),
        nullable=False
    )
    is_verified = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())


# --------------------
# ARTISAN PROFILE
# --------------------
class ArtisanProfile(db.Model):
    __tablename__ = "artisan_profiles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id"),
        nullable=False
    )
    bio = db.Column(db.Text())
    years_of_experience = db.Column(db.Integer())
    hourly_rate = db.Column(db.Integer())
    location = db.Column(db.Text())
    availability_status = db.Column(
        db.Enum("available", "busy", "offline")
    )
    average_rating = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    user = db.relationship("User", uselist=False)
    skills = db.relationship("ArtisanSkill", back_populates="artisan")


# --------------------
# CLIENT PROFILE
# --------------------
class ClientProfile(db.Model):
    __tablename__ = "client_profiles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id"),
        nullable=False
    )
    location = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    user = db.relationship("User", uselist=False)


# --------------------
# SKILL
# --------------------
class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text())

    artisans = db.relationship("ArtisanSkill", back_populates="skill")


# --------------------
# ARTISAN SKILL (JOIN TABLE)
# --------------------
class ArtisanSkill(db.Model):
    __tablename__ = "artisan_skills"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("artisan_profiles.id"),
        nullable=False
    )
    skill_id = db.Column(
        db.Integer(),
        db.ForeignKey("skills.id")
    )

    artisan = db.relationship("ArtisanProfile", back_populates="skills")
    skill = db.relationship("Skill", back_populates="artisans")


# --------------------
# SERVICE REQUEST
# --------------------
class ServiceRequest(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer(), primary_key=True)
    client_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    skill_id = db.Column(
        db.Integer(),
        db.ForeignKey("skills.id")
    )
    description = db.Column(db.Text())
    location = db.Column(db.Text())
    preferred_date = db.Column(db.DateTime())
    budget = db.Column(db.Integer())
    status = db.Column(
        db.Enum("pending", "accepted", "completed", "cancelled")
    )
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    client = db.relationship("User")
    skill = db.relationship("Skill")
    booking = db.relationship("Booking", back_populates="service_request", uselist=False)


# --------------------
# BOOKING
# --------------------
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer(), primary_key=True)
    service_request_id = db.Column(
        db.Integer(),
        db.ForeignKey("service_requests.id")
    )
    scheduled_date = db.Column(db.DateTime())
    agreed_price = db.Column(db.Integer())
    status = db.Column(
        db.Enum("active", "completed", "cancelled")
    )
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    service_request = db.relationship(
        "ServiceRequest",
        back_populates="booking",
        uselist=False
    )
    payment = db.relationship("Payment", back_populates="booking", uselist=False)
    review = db.relationship("Review", back_populates="booking", uselist=False)


# --------------------
# PAYMENT
# --------------------
class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer(), primary_key=True)
    booking_id = db.Column(
        db.Integer(),
        db.ForeignKey("bookings.id")
    )
    amount = db.Column(db.Integer())
    payment_method = db.Column(
        db.Enum("mpesa", "cash", "card")
    )
    payment_status = db.Column(
        db.Enum("pending", "paid", "failed")
    )
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    booking = db.relationship("Booking", back_populates="payment", uselist=False)


# --------------------
# REVIEW
# --------------------
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    booking_id = db.Column(
        db.Integer(),
        db.ForeignKey("bookings.id")
    )
    client_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    rating = db.Column(db.Integer())
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    booking = db.relationship("Booking", back_populates="review", uselist=False)
    client = db.relationship("User", foreign_keys=[client_id])
    artisan = db.relationship("User", foreign_keys=[artisan_id])


# --------------------
# ARTISAN AVAILABILITY
# --------------------
class ArtisanAvailability(db.Model):
    __tablename__ = "artisan_availabilities"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    day_of_week = db.Column(db.Text())
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    artisan = db.relationship("User")


# --------------------
# NOTIFICATION
# --------------------
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    message = db.Column(db.Text())
    is_read = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    user = db.relationship("User")


# --------------------
# ARTISAN VERIFICATION
# --------------------
class ArtisanVerification(db.Model):
    __tablename__ = "artisan_verifications"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id")
    )
    document_type = db.Column(db.Text())
    document_url = db.Column(db.Text())
    verification_status = db.Column(
        db.Enum("verified", "pending", "declined")
    )
    verified_at = db.Column(db.Boolean())

    artisan = db.relationship("User")
