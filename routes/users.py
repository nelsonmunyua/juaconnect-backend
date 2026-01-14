from flask_restful import Resource, reqparse
from models import User, db
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import generate_password_hash, check_password_hash



signup_parser = reqparse.RequestParser()
signup_parser.add_argument("name", required=True, type=str, help="Username is required")

signup_parser.add_argument("email", required=True, type=str, help="Email is required") 

signup_parser.add_argument("password_hash", required=True, type=str, help="Password is required")


class UserSignup(Resource):
    def post(self):
        try:
         # validate on the route level
            data = signup_parser.parse_args()

            # check for unique columns
            email = User.query.filter(User.email == data['email']).first()

            if email:
                return {"message" : "Email already taken"}, 422
            
            name = User.query.filter(User.name == data['name']).first()

            if name:
                return {"message" : "Name already taken"}, 422
            
            pw_hash = generate_password_hash(data['password_hash']).decode("utf-8")
        # hand over to sqlalchemy


        #     user = User(
        #     name = data['name'],
        #     password_hash = data['password_hash'],
        #     email = data['email']
        # )
            
            # delete the plain password
            del data['password_hash']

            # keyword arguments unpacking
            user = User(**data, password_hash=pw_hash)

            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully"}, 201
        
        except IntegrityError as e:
            print(str(e))
            return {"message" : "Missing Values", "error": "IntegrityError"}, 422

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", required=True, type=str, help="Email is required")
login_parser.add_argument("password_hash", required=True, type=str, help="Password is required")


class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        
        # 1. check if user email exists
        exists = User.query.filter(User.email == data['email']).first()

        if exists is None:
            return {"message" : "Invalid credentials or Invalid email or password"}, 401
        #2 Vaalidate password
        is_valid_password = check_password_hash(exists.password_hash, data['password_hash'])

        if not is_valid_password:
            return {"message" : "Invalide email or password"}, 401
        return {"message" : "Login successful", "data": exists.to_dict(rules=())}


class UsersResource(Resource):
    def get(self):
        users = User.query.all()

        return [u.to_dict(rules=("-password_hash",)) for u in users]

class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)

        return user.to_dict(rules=(
        '-password_hash',))


