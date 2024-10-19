from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'  # Redirects to login page if not authenticated

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # Load user from the database using the user_id stored in the session
        return User.query.get(int(user_id))

    from app.controllers import user_controller
    from app.controllers.auth import auth_bp

    app.register_blueprint(user_controller.user_bp)
    app.register_blueprint(auth_bp)

    return app
