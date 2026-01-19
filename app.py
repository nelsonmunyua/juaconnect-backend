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



# ========== REGISTER ROUTES ==========

# ========== START SERVER ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)