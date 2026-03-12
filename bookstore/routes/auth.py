from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from bookstore.models import User, db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Вход выполнен")
            return redirect(url_for("main.index"))
        flash("Неверный логин или пароль")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы")
    return redirect(url_for("main.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip()
        if User.query.filter_by(email=email).first():
            flash("Пользователь с таким email уже существует")
            return redirect(url_for("auth.register"))

        user = User(
            name=request.form["name"],
            email=email,
            phone=request.form.get("phone")
        )
        user.set_password(request.form["password"])

        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна")
        return redirect(url_for("auth.login"))

    return render_template("register.html")