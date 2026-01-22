from flask_restful import Resource, reqparse
from models import User, db
from flask_bcrypt import check_password_hash, generate_password_hash



class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="Username is required")
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('phone', required=True, help="Phone number is required")
    parser.add_argument('password', required=True, help="Password is required")
    #parser.add_argument('role', required=True, help="Role is required")

    def post(self):
        data = Signup.parser.parse_args()

        # Check uniqueness BEFORE creating user object
        username_exists = User.query.filter_by(username=data['username']).one_or_none()
        if username_exists:
            return {"message": "Username already exists", "status": "fail"}, 400
        
        email_exists = User.query.filter_by(email=data['email']).one_or_none()
        if email_exists:
            return {"message": "Email already exists", "status": "fail"}, 400
        
        phone_exists = User.query.filter_by(phone=data['phone']).one_or_none()
        if phone_exists:
            return {"message": "Phone number already taken", "status": "fail"}, 400
        
        # Hash password and set role after uniqueness checks
        hashed_password = generate_password_hash(data['password'])
        
        user = User(
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password,
            role='client'
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "Account created successfully", "status": "success", "user": user.to_dict(rules=('-password',))}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Unable to create account: {str(e)}", "status": "fail"}, 400

