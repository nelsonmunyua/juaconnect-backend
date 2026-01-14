from flask_restful import Resource, reqparse
from models import User, db



class RegisterResource(Resource):
    pass

class LoginForm(Resource):
    pass


class UsersResource(Resource):
    def get(self):
        users = User.query.all()

        return [u.to_dict() for u in users]

class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        return user.to_dict()


