from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import os
from models import db, User, Review, Booking, Service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artisan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False



CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)

class Home(Resource):
    def get(self):
        return {'message': 'Artisan Marketplace API', 'status': 'running'}
class Stats(Resource):
    def get(self):
        stats = {
            'artisans': User.query.filter_by(is_artisan=True).count(),
            'services': Service.query.filter_by(is_published=True).count(),
            'bookings': Booking.query.count(),
            'reviews': Review.query.count()
        }
        return make_response(jsonify(stats), 200)

# Services CRUD
class Services(Resource):
    def get(self):
        services = [service.to_dict() for service in Service.query.filter_by(is_published=True).all()]
        return make_response(jsonify(services), 200)
    
    def post(self):
        data = request.get_json()
        try:
            service = Service(
                title=data['title'],
                description=data['description'],
                price=float(data['price']),
                category=data['category'],
                duration=int(data['duration']),
                artisan_id=int(data['artisan_id'])
            )
            db.session.add(service)
            db.session.commit()
            return make_response(jsonify(service.to_dict()), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 400)

class ServiceById(Resource):
    def get(self, id):
        service = Service.query.get(id)
        if not service:
            return make_response({'error': 'Service not found'}, 404)
        return make_response(jsonify(service.to_dict()), 200)
    
    def patch(self, id):
        service = Service.query.get(id)
        if not service:
            return make_response({'error': 'Service not found'}, 404)
        
        data = request.get_json()
        for attr in data:
            if hasattr(service, attr):
                setattr(service, attr, data[attr])
        
        db.session.commit()
        return make_response(jsonify(service.to_dict()), 200)
    
    def delete(self, id):
        service = Service.query.get(id)
        if not service:
            return make_response({'error': 'Service not found'}, 404)
        
        db.session.delete(service)
        db.session.commit()
        return make_response('', 204)

# Users
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                is_artisan=bool(data.get('is_artisan', False)),
                bio=data.get('bio', '')
            )
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(user.to_dict()), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 400)

# Bookings
class Bookings(Resource):
    def get(self):
        bookings = [booking.to_dict() for booking in Booking.query.all()]
        return make_response(jsonify(bookings), 200)

    def post(self):
        data = request.get_json()
        try:
            booking = Booking(
                date=datetime.fromisoformat(data['date'].replace('Z', '+00:00')),
                notes=data.get('notes', ''),
                client_id=int(data['client_id']),
                service_id=int(data['service_id'])
            )
            db.session.add(booking)
            db.session.commit()
            return make_response(jsonify(booking.to_dict()), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 400)

class BookingById(Resource):
    def patch(self, id):
        booking = Booking.query.get(id)
        if not booking:
            return make_response({'error': 'Booking not found'}, 404)

        data = request.get_json()
        if 'status' in data:
            booking.status = data['status']

        db.session.commit()
        return make_response(jsonify(booking.to_dict()), 200)

# Reviews
class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(jsonify(reviews), 200)

    def post(self):
        data = request.get_json()
        try:
            review = Review(
                rating=int(data['rating']),
                comment=data.get('comment', ''),
                client_id=int(data['client_id']),
                artisan_id=int(data['artisan_id'])
            )
            db.session.add(review)
            db.session.commit()
            return make_response(jsonify(review.to_dict()), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 400)


# Artisan Dashboard
class ArtisanDashboard(Resource):
    def get(self, artisan_id):
        artisan = User.query.get(artisan_id)
        if not artisan or not artisan.is_artisan:
            return make_response({'error': 'Artisan not found'}, 404)
        
        services = Service.query.filter_by(artisan_id=artisan_id).all()
        bookings = Booking.query.filter(
            Booking.service_id.in_([s.id for s in services])
        ).all()
        reviews = Review.query.filter_by(artisan_id=artisan_id).all()
        
        completed_bookings = [b for b in bookings if b.status == 'completed']
        
        dashboard_data = {
            'artisan': artisan.to_dict(),
            'services': [s.to_dict() for s in services],
            'bookings': [b.to_dict() for b in bookings],
            'reviews': [r.to_dict() for r in reviews],
            'stats': {
                'total_services': len(services),
                'total_bookings': len(bookings),
                'pending_bookings': len([b for b in bookings if b.status == 'pending']),
                'average_rating': sum(r.rating for r in reviews) / len(reviews) if reviews else 0,
                'total_revenue': sum(b.service.price for b in completed_bookings)
            }
        }
        
        return make_response(jsonify(dashboard_data), 200)

# ========== REGISTER ROUTES ==========

# ========== START SERVER ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)