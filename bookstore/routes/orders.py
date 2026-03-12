from flask import Blueprint, render_template
from flask_login import current_user
from bookstore.models import Order
from flask import request, redirect, url_for
from bookstore.models import CartItem, Order, OrderItem, db
from flask_login import current_user

orders_bp = Blueprint("orders", __name__)

def get_user_id():
    if current_user.is_authenticated:
        return current_user.id
    return 1


@orders_bp.route("/orders")
def orders():

    user_id = get_user_id()

    user_orders = Order.query.filter_by(user_id=user_id).all()

    return render_template("orders.html", orders=user_orders)

@orders_bp.route("/checkout", methods=["GET","POST"])
def checkout():

    items = CartItem.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":

        order = Order(
            user_id=current_user.id,
            status="Создан",
            address=request.form.get("address")
        )

        db.session.add(order)
        db.session.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=item.book.id,
                quantity=item.quantity,
                price_at_purchase=item.book.price
            )

            db.session.add(order_item)

            db.session.delete(item)

        db.session.commit()

        return redirect(url_for("orders.orders"))

    return render_template("checkout.html")
