from flask import Blueprint, render_template, request
from bookstore.models import Book
from bookstore.models import Genre

catalog_bp = Blueprint("catalog", __name__)

@catalog_bp.route("/catalog")
def catalog_index():
    search = request.args.get("search", "").strip()

    if search:
        books = Book.query.filter(
            Book.title.ilike(f"%{search}%") |
            Book.author.ilike(f"%{search}%")
        ).all()
    else:
        books = Book.query.order_by(Book.title).all()

    return render_template("catalog.html", books=books, search=search)

@catalog_bp.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)

@catalog_bp.route("/genre/<int:genre_id>")
def genre(genre_id):

    genre = Genre.query.get_or_404(genre_id)
    books = genre.books

    return render_template(
        "catalog.html",
        books=books,
        genre=genre
    )