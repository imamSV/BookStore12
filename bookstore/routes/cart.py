from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bookstore.models import CartItem, Book, db

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/")
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", items=items)


@cart_bp.route("/add/<int:book_id>", methods=["POST"])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)

    cart_item = CartItem.query.filter_by(user_id=current_user.id, book_id=book_id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash("Книга добавлена в корзину")
    return redirect(url_for("catalog.catalog_index"))


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash("Нельзя удалить чужой товар")
        return redirect(url_for("cart.view_cart"))

    db.session.delete(item)
    db.session.commit()
    flash("Товар удалён")
    return redirect(url_for("cart.view_cart"))