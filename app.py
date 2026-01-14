from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_restful import Api
from routes.users import UsersResource, UserResource, UserSignup, UserLogin
from routes.service import ServicesResource, ServiceResource
from routes.booking import BookingsResource, BookingResource
from routes.review import ReviewsResource, ReviewResource




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///juaconnect.db"

app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)

# link db to the flask instance
db.init_app(app)
# initialize flask-restful
api = Api(app)
# db.init_app(app)
@app.route('/')
def index():
    return {'message' : 'Welcome to juaconnect  backend'}, 200


api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UserSignup, '/sing-up')
api.add_resource(UserLogin, '/login')

api.add_resource(ServicesResource, '/services')
api.add_resource(ServiceResource, '/services/<int:id>')

api.add_resource(BookingsResource, '/bookings')
api.add_resource(BookingResource, '/bookings/<int:id>')

api.add_resource(ReviewsResource, '/reviews')
api.add_resource(ReviewResource, '/reviews/<int:id>')










if __name__ == '__main__':
    app.run(port=5555, debug=True)