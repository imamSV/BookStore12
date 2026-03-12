from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bookstore.models import Review, db

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

@reviews_bp.route("/add/<int:book_id>", methods=["POST"])
@login_required
def add_review(book_id):
    text = request.form["text"]
    rating = int(request.form["rating"])
    review = Review(
        user_id=current_user.id,
        book_id=book_id,
        text=text,
        rating=rating
    )
    db.session.add(review)
    db.session.commit()
    flash("Отзыв добавлен")
    return redirect(url_for("catalog.book_detail", book_id=book_id))