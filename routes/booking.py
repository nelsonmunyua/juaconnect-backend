from flask_restful import Resource, reqparse
from models import Booking, db

# -------------------------
# Request parser
# -------------------------
booking_parser = reqparse.RequestParser()
booking_parser.add_argument("date", required=True, type=str, help="Date is required (YYYY-MM-DD HH:MM)")
booking_parser.add_argument("status", type=str, help="Status of booking")
booking_parser.add_argument("notes", type=str)
booking_parser.add_argument("client_id", required=True, type=int, help="Client ID is required")
booking_parser.add_argument("service_id", required=True, type=int, help="Service ID is required")

class BookingsResource(Resource):
    def get(self):
        bookings = Booking.query.all()

        # Same recursion-safe pattern as Users/Services
        return [b.to_dict() for b in bookings]

    def post(self):
        data = booking_parser.parse_args()

        # Convert date string to datetime
        from datetime import datetime
        try:
            date_obj = datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD HH:MM"}, 400

        booking = Booking(
            date=date_obj,
            status=data.get("status") or "pending",
            notes=data.get("notes"),
            client_id=data["client_id"],
            service_id=data["service_id"]
        )

        db.session.add(booking)
        db.session.commit()

        return booking.to_dict(), 201

class BookingResource(Resource):
    def get(self, id):
        booking = Booking.query.get(id)

        if not booking:
            return {"error": "Booking not found"}, 404

        # Recursion-safe serialization
        return booking.to_dict(rules=(
            '-client.bookings',
            '-service.bookings'
        ))
