from flask_restful import Resource, reqparse
from models import Review, db

# -------------------------
# Request parser 
# -------------------------
review_parser = reqparse.RequestParser()
review_parser.add_argument("rating", required=True, type=int, help="Rating 1-5 is required")
review_parser.add_argument("comment", type=str)
review_parser.add_argument("client_id", required=True, type=int, help="Client ID is required")
review_parser.add_argument("artisan_id", required=True, type=int, help="Artisan ID is required")


class ReviewsResource(Resource):
    def get(self):
        reviews = Review.query.all()

        # recursion-safe, same pattern
        return [r.to_dict() for r in reviews]

    def post(self):
        data = review_parser.parse_args()

        # Validate rating (1-5)
        if not 1 <= data["rating"] <= 5:
            return {"error": "Rating must be between 1 and 5"}, 400

        review = Review(
            rating=data["rating"],
            comment=data.get("comment"),
            client_id=data["client_id"],
            artisan_id=data["artisan_id"]
        )

        db.session.add(review)
        db.session.commit()

        return review.to_dict(), 201

class ReviewResource(Resource):
    def get(self, id):
        review = Review.query.get(id)

        if not review:
            return {"error": "Review not found"}, 404

        # recursion-safe
        return review.to_dict(rules=(
            '-client.reviews_received',
            '-artisan.reviews_received',
            '-services'
        ))
