# JuaConnect Backend API

JuaConnect is a comprehensive backend service designed to connect clients with skilled artisans and service professionals. The platform enables users to browse services, book appointments, and leave reviews in a seamless marketplace experience.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Configuration](#configuration)
- [Data Seeding](#data-seeding)

---

## 🎯 Project Overview

JuaConnect Backend is a Flask-based REST API that serves as the backend for a two-sided marketplace platform. It facilitates connections between:

- **Artisans/Service Providers**: Skilled professionals offering services like plumbing, electrical work, carpentry, etc.
- **Clients**: Users seeking professional services for their needs

The platform tracks services, bookings, user profiles, and customer reviews to build a trusted community.

---

## 🏗️ Architecture

The application follows a RESTful architecture with the following components:

- **Flask Framework**: Lightweight Python web framework
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **Flask-RESTful**: Extension for building REST APIs
- **SQLite Database**: Lightweight database for development
- **Flask-Migrate**: Database migration management with Alembic
- **CORS Support**: Cross-origin resource sharing for frontend integration

---

## 💾 Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Pipenv (recommended)

### Step 1: Clone and Navigate to Project

```bash
cd /home/user/development/code/phase4/juaconnect-backend
```

### Step 2: Install Dependencies

Using Pipenv (recommended):

```bash
pipenv install
pipenv shell
```

Or using pip:

```bash
pip install flask flask-restful flask-migrate sqlalchemy-serializer flask-sqlalchemy flask-bcrypt flask-cors
```

### Step 3: Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 4: Seed Sample Data (Optional)

```bash
python seed.py
```

This creates sample users, services, bookings, and reviews for testing.

### Step 5: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5555` with debug mode enabled.

---

## 🌐 API Endpoints

All endpoints return JSON responses. The base URL is `http://localhost:5555`.

### Authentication Endpoints

#### User Signup

- **URL**: `/sign-up`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "name": "string (required, unique)",
    "email": "string (required, unique)",
    "password_hash": "string (required)"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "message": "User created successfully"
  }
  ```

#### User Login

- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "string (required)",
    "password_hash": "string (required)"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "data": { "user_object" }
  }
  ```

### Users Endpoints

#### Get All Users

- **URL**: `/users`
- **Method**: `GET`
- **Response**: `200 OK` - Array of user objects (excludes password_hash)

#### Get User by ID

- **URL**: `/users/<id>`
- **Method**: `GET`
- **Response**: `200 OK` - User object
  ```json
  {
    "id": 1,
    "name": "John Artisan",
    "role": "artisan",
    "email": "john@artisan.com",
    "bio": "Experienced plumber...",
    "profile_picture": "URL",
    "phone": "+254712345678",
    "location": "Nairobi, Kenya",
    "skills": "Plumbing, Pipe Installation...",
    "experience_years": 12,
    "business_name": "John's Quality Plumbing",
    "business_address": "123 Pipeline Road...",
    "tax_id": "A123456789X",
    "hourly_rate": 2500.0,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
  ```

### Services Endpoints

#### Get All Services

- **URL**: `/services`
- **Method**: `GET`
- **Response**: `200 OK` - Array of service objects

#### Get Service by ID

- **URL**: `/services/<id>`
- **Method**: `GET`
- **Response**: `200 OK` - Service object
  ```json
  {
    "id": 1,
    "title": "Pipe Installation",
    "description": "Professional pipe installation...",
    "price": 5000.0,
    "category": "Plumbing",
    "duration": 120,
    "artisan_id": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
  ```

#### Create Service

- **URL**: `/services`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "title": "string (required)",
    "description": "string",
    "price": "float (required)",
    "category": "string",
    "duration": "integer (minutes)",
    "artisan_id": "integer (required)"
  }
  ```
- **Response**: `201 Created` - Created service object

### Bookings Endpoints

#### Get All Bookings

- **URL**: `/bookings`
- **Method**: `GET`
- **Response**: `200 OK` - Array of booking objects

#### Get Booking by ID

- **URL**: `/bookings/<id>`
- **Method**: `GET`
- **Response**: `200 OK` - Booking object
  ```json
  {
    "id": 1,
    "date": "2024-02-20T14:00:00",
    "status": "pending",
    "notes": "Please call before arrival",
    "client_id": 3,
    "service_id": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
  ```

#### Create Booking

- **URL**: `/bookings`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "date": "string (required, format: YYYY-MM-DD HH:MM)",
    "status": "string (optional)",
    "notes": "string",
    "client_id": "integer (required)",
    "service_id": "integer (required)"
  }
  ```
- **Response**: `201 Created` - Created booking object

### Reviews Endpoints

#### Get All Reviews

- **URL**: `/reviews`
- **Method**: `GET`
- **Response**: `200 OK` - Array of review objects

#### Get Review by ID

- **URL**: `/reviews/<id>`
- **Method**: `GET`
- **Response**: `200 OK` - Review object
  ```json
  {
    "id": 1,
    "rating": 5,
    "comment": "Excellent work, highly recommended!",
    "client_id": 3,
    "artisan_id": 1,
    "helpful_count": 12,
    "created_at": "2024-01-20T15:45:00",
    "updated_at": "2024-01-20T15:45:00"
  }
  ```

#### Create Review

- **URL**: `/reviews`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "rating": "integer (required, 1-5)",
    "comment": "string",
    "client_id": "integer (required)",
    "artisan_id": "integer (required)"
  }
  ```
- **Response**: `201 Created` - Created review object

### Health Check

#### Root Endpoint

- **URL**: `/`
- **Method**: `GET`
- **Response**: `200 OK`
  ```json
  {
    "message": "Welcome to juaconnect backend"
  }
  ```

---

## 💾 Database Models

### User Model

Represents both artisans and clients in the system.

**Fields**:

- `id` (Integer, PK)
- `name` (String, unique, required)
- `role` (Enum: "client", "artisan", default: "client")
- `email` (String, unique, required)
- `password_hash` (String, hashed password)
- `bio` (Text, professional biography)
- `profile_picture` (String, URL to profile image)
- `phone` (String, contact number)
- `location` (String, geographic location)
- `skills` (Text, comma-separated list of skills)
- `experience_years` (Integer, years of professional experience)
- `business_name` (String, artisan business name)
- `business_address` (Text, business location)
- `tax_id` (String, tax identification for professionals)
- `hourly_rate` (Float, service rate per hour)
- `created_at` (DateTime, auto-set on creation)
- `updated_at` (DateTime, auto-updated on modification)

**Relationships**:

- `services`: One-to-many with Service (artisan's services)
- `bookings`: One-to-many with Booking (client's bookings)
- `reviews_received`: One-to-many with Review (reviews of artisan)

**Validations**:

- Email must contain "@" symbol
- Username must be at least 3 characters

---

### Service Model

Represents services offered by artisans.

**Fields**:

- `id` (Integer, PK)
- `title` (String, required)
- `description` (Text, service details)
- `price` (Float, required, must be non-negative)
- `category` (String, service category)
- `duration` (Integer, service duration in minutes)
- `artisan_id` (Integer, FK to User)
- `created_at` (DateTime, auto-set on creation)
- `updated_at` (DateTime, auto-updated on modification)

**Relationships**:

- `artisan`: Many-to-one with User
- `bookings`: One-to-many with Booking
- `reviews`: Many-to-many with Review

**Validations**:

- Price must be non-negative

---

### Booking Model

Represents a service booking/appointment.

**Fields**:

- `id` (Integer, PK)
- `date` (DateTime, required)
- `status` (String, default: "pending", options: pending, confirmed, completed, cancelled)
- `notes` (Text, booking notes/instructions)
- `client_id` (Integer, FK to User)
- `service_id` (Integer, FK to Service)
- `created_at` (DateTime, auto-set on creation)
- `updated_at` (DateTime, auto-updated on modification)

**Relationships**:

- `client`: Many-to-one with User
- `service`: Many-to-one with Service

---

### Review Model

Represents customer reviews of artisans and their services.

**Fields**:

- `id` (Integer, PK)
- `rating` (Integer, required, 1-5 stars)
- `comment` (Text, review comment)
- `client_id` (Integer, FK to User)
- `artisan_id` (Integer, FK to User)
- `helpful_count` (Integer, number of helpful votes, default: 0)
- `created_at` (DateTime, auto-set on creation)
- `updated_at` (DateTime, auto-updated on modification)

**Relationships**:

- `client`: Many-to-one with User
- `artisan`: Many-to-one with User
- `services`: Many-to-many with Service

**Validations**:

- Rating must be between 1 and 5

---

## 📁 Project Structure

```
juaconnect-backend/
├── app.py                 # Flask application entry point
├── models.py              # SQLAlchemy database models
├── seed.py               # Sample data seeding script
├── Pipfile               # Pipenv dependencies and Python version
├── README.md             # This file
├── instance/             # Instance-specific files (database, config)
│   └── juaconnect.db    # SQLite database file
├── migrations/           # Database migration files
│   ├── alembic.ini      # Alembic configuration
│   ├── env.py           # Migration environment configuration
│   ├── script.py.mako   # Migration script template
│   └── versions/        # Migration version files
└── routes/              # API route handlers
    ├── users.py         # User authentication and management
    ├── service.py       # Service CRUD operations
    ├── booking.py       # Booking management
    └── review.py        # Review management
```

---

## ✨ Features

### Authentication

- Secure user registration with password hashing (Flask-Bcrypt)
- Email-based login with password verification
- Unique email and username validation

### User Management

- Role-based users (Artisan and Client)
- Comprehensive artisan profiles with skills and experience
- Business information for professional artisans
- Profile pictures and location tracking

### Service Management

- Create and browse services
- Service categorization and pricing
- Service duration tracking
- Multiple services per artisan

### Booking System

- Schedule service appointments
- Flexible date/time selection
- Booking status tracking (pending, confirmed, completed, cancelled)
- Notes for special instructions

### Review System

- 5-star rating system
- Written feedback on services
- Helpful count tracking
- Many-to-many relationship with services

### Database Features

- Automatic timestamp tracking (created_at, updated_at)
- Data validation at model level
- Recursive serialization protection
- SQLAlchemy ORM for safe queries
- Migration support with Flask-Migrate

### API Features

- RESTful endpoint design
- CORS enabled for frontend integration
- JSON request/response format
- Error handling with appropriate HTTP status codes
- Request validation with Flask-RESTful

---

## 🛠️ Technology Stack

| Technology            | Purpose                           |
| --------------------- | --------------------------------- |
| Flask 2.x             | Web framework                     |
| Flask-RESTful         | REST API building                 |
| SQLAlchemy            | ORM and database queries          |
| Flask-SQLAlchemy      | SQLAlchemy integration with Flask |
| Flask-Migrate         | Database migrations               |
| Flask-Bcrypt          | Password hashing                  |
| Flask-CORS            | Cross-origin requests             |
| SQLAlchemy-Serializer | JSON serialization                |
| SQLite                | Database (development)            |
| Python 3.8+           | Programming language              |

---

## ⚙️ Configuration

### Database Configuration

```python
# In app.py
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///juaconnect.db"
app.config["SQLALCHEMY_ECHO"] = True  # SQL query logging
```

- **Database Location**: `instance/juaconnect.db`
- **Type**: SQLite (suitable for development)
- **Echo Mode**: Enabled (logs all SQL queries to console)

### Server Configuration

```python
# In app.py
if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

- **Port**: 5555
- **Debug Mode**: Enabled (auto-reload on code changes)
- **Host**: localhost (127.0.0.1)

---

## 🌱 Data Seeding

The `seed.py` script populates the database with sample data for testing:

### Sample Data Created

**Artisans**:

- John Artisan (Plumber) - 12 years experience
- Mary Artisan (Electrician) - 8 years experience
- Paul Carpenter (Carpenter) - 15 years experience

**Clients**:

- Alice Client (Homeowner)
- Bob Client (Property Manager)

**Services**: Multiple services from each artisan with varying prices

**Bookings**: Sample appointments with different statuses

**Reviews**: Customer feedback with ratings

### Running the Seed

```bash
python seed.py
```

Output includes progress indicators:

- 🌱 Clearing existing data
- 👤 Creating users
- 🔧 Creating services
- 📅 Creating bookings
- ⭐ Creating reviews

**Note**: Running the seed script will clear all existing data. Use only in development.

---

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

- Server runs on `http://localhost:5555`
- Debug mode is enabled
- Auto-reload on code changes
- SQL queries logged to console

### Test API Endpoints

You can test the API using:

**cURL**:

```bash
curl http://localhost:5555/
```

**Postman**: Import the API endpoints for testing

**Python requests**:

```python
import requests

response = requests.get('http://localhost:5555/users')
print(response.json())
```

---

## 📝 Notes

- Password hashing is handled via Flask-Bcrypt for security
- Serialization rules prevent infinite recursion when returning related objects
- The database is automatically created on first run
- All timestamps are automatically managed by SQLAlchemy
- CORS is enabled to allow frontend applications to communicate with this backend

---

## 📞 Support & Troubleshooting

### Common Issues

**Database Locked Error**:

- Close all active connections to the database
- Delete `instance/juaconnect.db` and reinitialize

**Port Already in Use**:

- Change port in `app.py`: `app.run(port=5556)`
- Or kill the process using port 5555

**Import Errors**:

- Ensure all dependencies are installed: `pipenv install` or `pip install -r requirements.txt`
- Verify Python version is 3.8+

**Migration Issues**:

- Reset migrations: Delete `migrations/versions/*` and re-run `flask db migrate`

---

## 📄 License

This project is part of the JuaConnect platform.

---

**Last Updated**: January 2026
**Version**: 1.0.0
