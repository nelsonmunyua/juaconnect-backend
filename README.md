# JuaConnect Backend

A Flask-based REST API for an artisan marketplace platform that connects clients with skilled artisans. The backend manages users, services, bookings, and reviews.

## Overview

JuaConnect is a comprehensive artisan marketplace backend that enables:

- User registration and management (clients and artisans)
- Service listing and management by artisans
- Booking system for clients to book artisan services
- Rating and review system for quality assurance
- Artisan dashboard with analytics and statistics

## Tech Stack

- **Framework**: Flask 3.x
- **Database**: SQLite with SQLAlchemy ORM
- **API**: Flask-RESTful
- **Database Migrations**: Flask-Migrate (Alembic)
- **Authentication**: Flask-Bcrypt
- **CORS**: Flask-CORS
- **Serialization**: SQLAlchemy-Serializer
- **Environment**: Python 3.8



## Models

### User

- `id`: Primary key
- `username`: Unique username (min 3 characters)
- `email`: Unique email address (validated format)
- `password_hash`: Bcrypt hashed password
- `is_artisan`: Boolean flag to identify artisans
- `bio`: User biography/description
- `created_at`: Timestamp of account creation
- **Relationships**: Services, Bookings, Reviews

### Service

- `id`: Primary key
- `title`: Service name
- `description`: Service details
- `price`: Service cost (must be non-negative)
- `category`: Service category
- `duration`: Duration in minutes
- `is_published`: Publication status
- `created_at`: Creation timestamp
- `artisan_id`: Foreign key to User
- **Relationships**: Bookings

### Booking

- `id`: Primary key
- `date`: Booking date/time
- `status`: Booking status (pending, confirmed, completed, cancelled)
- `notes`: Additional notes
- `created_at`: Creation timestamp
- `client_id`: Foreign key to User (client)
- `service_id`: Foreign key to Service
- **Relationships**: Client, Service

### Review

- `id`: Primary key
- `rating`: Rating 1-5 (validated)
- `comment`: Review comment
- `helpful_count`: Count of helpful votes
- `created_at`: Creation timestamp
- `client_id`: Foreign key to User (reviewer)
- `artisan_id`: Foreign key to User (artisan being reviewed)

## API Endpoints

### Home & Stats

- `GET /` - API health check
- `GET /stats` - Get platform statistics (artisans, services, bookings, reviews count)

### Services

- `GET /services` - List all published services
- `POST /services` - Create a new service
- `GET /services/<id>` - Get service details
- `PATCH /services/<id>` - Update service
- `DELETE /services/<id>` - Delete service

### Users

- `GET /users` - List all users
- `POST /users` - Create new user

### Bookings

- `GET /bookings` - List all bookings
- `POST /bookings` - Create a new booking
- `PATCH /bookings/<id>` - Update booking status

### Reviews

- `GET /reviews` - List all reviews
- `POST /reviews` - Create a new review

### Artisan Dashboard

- `GET /artisan/<artisan_id>` - Get artisan dashboard with stats:
  - Services offered
  - All bookings
  - Reviews received
  - Booking statistics (pending, completed)
  - Average rating
  - Total revenue from completed bookings

## Installation

### Prerequisites

- Python 3.8 or higher
- Pipenv

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd juaconnect-backend
   ```

2. **Create virtual environment (using Pipenv)**

   ```bash
   pipenv install
   pipenv shell
   ```


3. **Initialize the database**

   ```bash
   flask db upgrade
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The API will start at `http://localhost:5555`

## Configuration

The application uses the following configurations:

- **Database**: SQLite at `instance/artisan.db`
- **CORS**: Enabled for `http://localhost:5174` (frontend)
- **Debug Mode**: Enabled for development
- **Port**: 5555


## Database Migrations

The project uses Flask-Migrate for database schema management.

### Create a new migration

```bash
flask db migrate -m "Description of changes"
```

### Apply migrations

```bash
flask db upgrade
```


## CORS Configuration

The backend is configured to accept requests from `http://localhost:5174` by default. To modify CORS settings, update the `CORS()` configuration in `app.py`:

```python
CORS(app, resources={r"/*": {"origins": "http://your-frontend-url"}})
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - OK (successful GET/PATCH)
- `201` - Created (successful POST)
- `204` - No Content (successful DELETE)
- `400` - Bad Request (validation errors)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## Development

### Running in Development Mode

The application starts with `debug=True` by default, enabling:

- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Testing

To test the API endpoints, use:

- Postman

## Future Enhancements

- User authentication and JWT tokens
- Payment processing
- Email notifications
- Image uploads for services and profiles
- Advanced search and filtering
- Real-time notifications
- User ratings and badges
- Service categories and subcategories
- Dispute resolution system

## Contributors

- Nelson Munyua
- Joyce Njogu
- Nicole Kibe
- Hillary Ating'o
- Peter Emu
- Newton Orina

## Frontend link
https://github.com/nelsonmunyua/juaconnect-frontend

## License

MIT
