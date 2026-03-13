from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bookstore.models import Order, OrderItem, CartItem, db

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/")
@login_required
def orders():

    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("orders.html", orders=user_orders)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Корзина пуста")
        return redirect(url_for("cart.view_cart"))

    if request.method == "POST":
        delivery_type = request.form["delivery_type"]
        address = request.form.get("address") if delivery_type == "delivery" else None

        order = Order(
            user_id=current_user.id,
            delivery_type=delivery_type,
            address=address
        )

        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=item.book_id,
                quantity=item.quantity,
                price_at_purchase=item.book.price
            )
            db.session.add(order_item)

        if delivery_type == "delivery" and not address:
            flash("Введите адрес доставки")
            return redirect(url_for("orders.checkout"))


        for item in cart_items:
            db.session.delete(item)

        db.session.commit()
        flash("Заказ успешно оформлен")
        return redirect(url_for("orders.orders"))

    return render_template("checkout.html", cart_items=cart_items)
