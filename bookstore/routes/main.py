from flask import Blueprint, render_template, request
from bookstore.models import Book, Genre

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():

    search = request.args.get("search")

    if search:
        books = Book.query.filter(Book.title.ilike(f"%{search}%")).all()
    else:
        books = Book.query.all()

    top_books = Book.query.order_by(Book.rating.desc()).limit(3).all()
    genres = Genre.query.all()

    return render_template(
        "index.html",
        top_books=top_books,
        genres=genres,
        books=books
    )