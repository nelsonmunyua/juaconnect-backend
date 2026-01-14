from flask import Flask,jsonify
from flask_migrate import Migrate
from models import db,Notification
from flask_restful import Api
from routes.users import UsersResource, UserResource

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

# 🔔 Get all notifications (TEMP: client_id = 1)
@app.route('/client/notifications', methods=['GET'])
def get_notifications():
    client_id = 1  # TEMP: hardcoded client ID
    notifications = Notification.query.filter_by(user_id=client_id)\
                    .order_by(Notification.created_at.desc()).all()
    
    # Convert to list of dicts
    data = [n.to_dict() for n in notifications]

    return jsonify(data), 200


# ✅ Mark notification as read
@app.route('/client/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    client_id = 1
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=client_id
    ).first()

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read"}), 200


api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:id>' )








if __name__ == '__main__':
    app.run(port=5555, debug=True)