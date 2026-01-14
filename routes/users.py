from flask_restful import Resource, reqparse
from models import User, db

signup_parser = reqparse.RequestParser()
signup_parser.add_argument("username", required=True, type=str, help="Username is required")

signup_parser.add_argument("email", required=True, type=str,
                           help="Email is required") 


class UserSignup(Resource):
    def post(self):

        data = signup_parser


class LoginForm(Resource):
    pass


class UsersResource(Resource):
    def get(self):
        users = User.query.all()

        return [u.to_dict() for u in users]

class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        return user.to_dict(rules=(
        '-password',))


