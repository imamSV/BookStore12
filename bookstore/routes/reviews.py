from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bookstore.models import Review, Book, db

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")


@reviews_bp.route("/add/<int:book_id>", methods=["POST"])
@login_required
def add_review(book_id):

    rating = int(request.form["rating"])
    text = request.form["text"]

    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        book_id=book_id
    ).first()

    if existing_review:
        flash("Вы уже оставили отзыв на эту книгу")
        return redirect(url_for("catalog.book_detail", book_id=book_id))

    review = Review(
        user_id=current_user.id,
        book_id=book_id,
        rating=rating,
        text=text
    )

    db.session.add(review)

    book = Book.query.get(book_id)

    if book.rating_count is None:
        book.rating_count = 0
    if book.rating is None:
        book.rating = 0

    book.rating_count += 1
    book.rating = (
        (book.rating * (book.rating_count - 1)) + rating
    ) / book.rating_count

    db.session.commit()

    flash("Отзыв добавлен")
    return redirect(url_for("catalog.book_detail", book_id=book_id))