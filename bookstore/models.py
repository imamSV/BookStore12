from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bookstore import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cart_items = db.relationship("CartItem", backref="cart_items")
    orders = db.relationship("Order", backref="user", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, index=True)


class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))
    rating = db.Column(db.Float, default=0)
    rating_count = db.Column(db.Integer, default=0)
    genres = db.relationship(
        "Genre",
        secondary=book_genres,
        backref="books"
    )
    reviews = db.relationship("Review", backref="book", lazy=True)


class CartItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        index=True
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id")
    )

    quantity = db.Column(db.Integer, default=1)

    book = db.relationship("Book")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(db.String(50), default="processing")
    delivery_type = db.Column(db.String(50))
    address = db.Column(db.String(255))
    items = db.relationship("OrderItem", backref="order", lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id")
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id")
    )
    quantity = db.Column(db.Integer)
    price_at_purchase = db.Column(db.Numeric(10, 2))
    book = db.relationship("Book")


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        index=True
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id"),
        index=True
    )

    text = db.Column(db.Text)
    rating = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )