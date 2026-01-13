from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
#from sqlalchemy.orm import validates

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
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.Text(), nullable=False)
    phone_number = db.Column(db.Text(), nullable=False, unique=True)
    email = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(
        db.Enum("client", "artisan", "admin"), default="client",
        nullable=False
    )
    is_verified = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    # Relationships
    artisan = db.relationship("ArtisanProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    client = db.relationship("ClientProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # One-to-many : User can create multiple service requests
    service_requests = db.relationship("ServiceRequest", back_populates="client", foreign_keys="ServiceRequest.client_id")

    # one to many: User (as artisan) can have multiple bookings
    bookings_as_client =db.relationship("Booking", back_populates="client", foreign_keys="Booking.client_id")


# --------------------
# ARTISAN PROFILE
# --------------------
class ArtisanProfile(db.Model, SerializerMixin):
    __tablename__ = "artisan_profiles"

    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Text(), nullable=False)

    role = db.Column(
        db.Enum("client", "artisan", "admin", name="user_roles"),
        default="client",
        nullable=False
    )

    is_verified = db.Column(db.Boolean(), default=False)

    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    artisan_profile = db.relationship(
        "ArtisanProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    client_profile = db.relationship(
        "ClientProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )




# --------------------
# CLIENT PROFILE
# --------------------
class ClientProfile(db.Model, SerializerMixin):
    __tablename__ = "client_profiles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    location = db.Column(db.String(255))

    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    user = db.relationship("User", back_populates="client_profile")

    service_requests = db.relationship(
        "ServiceRequest",
        back_populates="client",
        cascade="all, delete-orphan"
    )





# --------------------
# SKILL
# --------------------
class Skill(db.Model, SerializerMixin):
    __tablename__ = "skills"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())

    artisans = db.relationship(
        "ArtisanSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )




# --------------------
# ARTISAN SKILL (JOIN TABLE)
# --------------------
class ArtisanSkill(db.Model, SerializerMixin):
    __tablename__ = "artisan_skills"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("artisan_profiles.id"),
        nullable=False
    )
    skill_id = db.Column(
        db.Integer(),
        db.ForeignKey("skills.id"),
        nullable=False
    )

    artisan = db.relationship("ArtisanProfile", back_populates="skills")
    skill = db.relationship("Skill", back_populates="artisans")



# --------------------
# SERVICE REQUEST
# --------------------
class ServiceRequest(db.Model, SerializerMixin):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer(), primary_key=True)

    client_id = db.Column(
        db.Integer(),
        db.ForeignKey("client_profiles.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer(),
        db.ForeignKey("skills.id"),
        nullable=False
    )

    description = db.Column(db.Text())
    location = db.Column(db.String(255))
    preferred_date = db.Column(db.DateTime())
    budget = db.Column(db.Integer())

    status = db.Column(
        db.Enum("pending", "accepted", "completed", "cancelled", name="request_status"),
        default="pending"
    )

    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    client = db.relationship("ClientProfile", back_populates="service_requests")
    skill = db.relationship("Skill")

    booking = db.relationship(
        "Booking",
        back_populates="service_request",
        uselist=False
    )

# --------------------
# BOOKING
# --------------------
class Booking(db.Model, SerializerMixin):
    __tablename__ = "bookings"

    id = db.Column(db.Integer(), primary_key=True)

    service_request_id = db.Column(
        db.Integer(),
        db.ForeignKey("service_requests.id"),
        nullable=False,
        unique=True
    )

    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("artisan_profiles.id"),
        nullable=False
    )

    scheduled_date = db.Column(db.DateTime())
    agreed_price = db.Column(db.Integer())

    status = db.Column(
        db.Enum("active", "completed", "cancelled", name="booking_status"),
        default="active"
    )

    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    service_request = db.relationship("ServiceRequest", back_populates="booking")
    artisan = db.relationship("ArtisanProfile", back_populates="bookings")

    payment = db.relationship(
        "Payment",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )

    review = db.relationship(
        "Review",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )


# --------------------
# PAYMENT
# --------------------
class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"

    id = db.Column(db.Integer(), primary_key=True)
    booking_id = db.Column(
        db.Integer(),
        db.ForeignKey("bookings.id"),
        nullable=False,
        unique=True
    )

    amount = db.Column(db.Integer(), nullable=False)

    payment_method = db.Column(
        db.Enum("mpesa", "cash", "card", name="payment_method"),
        nullable=False
    )

    payment_status = db.Column(
        db.Enum("pending", "paid", "failed", name="payment_status"),
        default="pending"
    )

    created_at = db.Column(db.DateTime(), server_default=db.func.now())

    booking = db.relationship("Booking", back_populates="payment")

# --------------------
# REVIEW
# --------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    rating = db.Column(db.Integer())
    comment = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    
    booking_id = db.Column(
        db.Integer(),
        db.ForeignKey("bookings.id"), nullable=False, unique=True
    )
    client_id = db.Column(
        db.Integer(),
        db.ForeignKey("client_profiles.id"), nullable=False
    )
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("artisan_profiles.id"), nullable=False
    )

    booking = db.relationship("Booking", back_populates="review")
    client = db.relationship("ClientProfile")
    artisan = db.relationship("ArtisanProfile")


# --------------------
# ARTISAN AVAILABILITY
# --------------------
class ArtisanAvailability(db.Model, SerializerMixin):
    __tablename__ = "artisan_availabilities"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id"), nullable=False
    )
    day_of_week = db.Column(
        db.Enum(
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday",
            name="days_of_week"
        ),
        nullable=False
    )
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    

    artisan = db.relationship("ArtisanProfile", back_populates="availability")


# --------------------
# NOTIFICATION
# --------------------
class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id"), nullable=False
    )
    message = db.Column(db.Text(), nullable=False)
    is_read = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    

    user = db.relationship("User")


# --------------------
# ARTISAN VERIFICATION
# --------------------
class ArtisanVerification(db.Model, SerializerMixin):
    __tablename__ = "artisan_verifications"

    id = db.Column(db.Integer(), primary_key=True)
    artisan_id = db.Column(
        db.Integer(),
        db.ForeignKey("artisan_profiles.id"), nullable=False
    )
    document_type = db.Column(db.String(100))
    document_url = db.Column(db.Text())
    verification_status = db.Column(
        db.Enum("verified", "pending", "declined", name="verification_status"), default="pending"
    )
    verified_at = db.Column(db.DateTime)

    artisan = db.relationship("ArtisanProfile")
