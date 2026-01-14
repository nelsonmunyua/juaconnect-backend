from flask_restful import Resource, reqparse
from models import Service, db

service_parser = reqparse.RequestParser()
service_parser.add_argument("title", required=True, type=str, help="Title is required")
service_parser.add_argument("description", type=str)
service_parser.add_argument("price", required=True, type=float, help="Price is required")
service_parser.add_argument("category", type=str)
service_parser.add_argument("duration", type=int)
service_parser.add_argument("artisan_id", required=True, type=int, help="Artisan ID is required")

class ServicesResource(Resource):
    def get(self):
        services = Service.query.all()

        # SAME style as users.py
        return [s.to_dict() for s in services]

    def post(self):
        data = service_parser.parse_args()

        service = Service(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            category=data["category"],
            duration=data["duration"],
            artisan_id=data["artisan_id"]
        )

        db.session.add(service)
        db.session.commit()

        return service.to_dict(), 201
class ServiceResource(Resource):
    def get(self, id):
        service = Service.query.get(id)

        if not service:
            return {"error": "Service not found"}, 404

        # SAME recursion-stop pattern as UserResource
        return service.to_dict(rules=(
            '-artisan',
            '-bookings',
            '-reviews'
        ))
