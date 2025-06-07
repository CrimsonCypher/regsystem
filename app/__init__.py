from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from . import views, admin
        app.register_blueprint(views.bp)
        app.register_blueprint(admin.admin_bp)
        db.create_all()

    return app
