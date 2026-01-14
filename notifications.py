# notifications.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Notification, db

# Define the blueprint
notifications_bp = Blueprint("notifications", __name__, url_prefix="/client/notifications")

# ---------------------------
# Get all notifications
# ---------------------------
@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    client_id = get_jwt_identity()  # Assuming JWT stores User.id
    notifications = Notification.query.filter_by(user_id=client_id).order_by(Notification.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notifications]), 200

# ---------------------------
# Mark a notification as read
# ---------------------------
@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_notification_read(notification_id):
    client_id = get_jwt_identity()
    notification = Notification.query.filter_by(id=notification_id, user_id=client_id).first()
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read"}), 200
