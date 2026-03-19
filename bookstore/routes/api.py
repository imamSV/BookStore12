from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from bookstore.models import Book, CartItem, Order

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/books")
def get_books():
    books = Book.query.all()

    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "price": float(b.price),
            "rating": b.rating
        }
        for b in books
    ])


@api_bp.route("/books/<int:book_id>")
def get_book(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "price": float(book.price),
        "description": book.description,
        "rating": book.rating
    })


@api_bp.route("/cart")
@login_required
def get_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()

    return jsonify([
        {
            "book": item.book.title,
            "quantity": item.quantity,
            "price": float(item.book.price)
        }
        for item in items
    ])


@api_bp.route("/orders")
@login_required
def get_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    return jsonify([
        {
            "id": order.id,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "book": item.book.title,
                    "quantity": item.quantity,
                    "price": float(item.price_at_purchase)
                }
                for item in order.items
            ]
        }
        for order in orders
    ])