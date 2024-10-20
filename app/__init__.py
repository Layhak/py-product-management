from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='templates')  # Ensure this points to the correct folder
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.controllers.user_controller import user_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.home_controller import home_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    CORS(app, supports_credentials=True)

    return app
