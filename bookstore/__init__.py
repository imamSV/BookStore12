from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


    from bookstore.routes.main import main_bp
    from bookstore.routes.auth import auth_bp
    from bookstore.routes.catalog import catalog_bp
    from bookstore.routes.cart import cart_bp
    from bookstore.routes.orders import orders_bp
    from bookstore.routes.reviews import reviews_bp
    from bookstore.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(api_bp)


    return app