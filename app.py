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


# ========== REGISTER ROUTES ==========

# ========== START SERVER ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)