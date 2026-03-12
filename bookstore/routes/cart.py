from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from bookstore.models import CartItem, db

cart_bp = Blueprint("cart", __name__)

def get_user_id():
    if current_user.is_authenticated:
        return current_user.id
    return 1  # тестовый пользователь


@cart_bp.route("/cart")
def view_cart():
    user_id = get_user_id()

    items = CartItem.query.filter_by(user_id=user_id).all()
    total = sum(item.book.price * item.quantity for item in items)

    return render_template("cart.html", items=items, total=total)


@cart_bp.route("/cart/add/<int:book_id>")
def add_to_cart(book_id):

    user_id = get_user_id()

    item = CartItem.query.filter_by(
        user_id=user_id,
        book_id=book_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = CartItem(
            user_id=user_id,
            book_id=book_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()

    flash("Книга добавлена в корзину")

    return redirect(url_for("catalog.catalog_index"))


@cart_bp.route("/cart/remove/<int:item_id>")
def remove_from_cart(item_id):

    item = CartItem.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    flash("Книга удалена из корзины")

    return redirect(url_for("cart.view_cart"))