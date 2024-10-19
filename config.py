import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:{os.environ.get('MYSQL_ROOT_PASSWORD')}@localhost:3306/{os.environ.get('MYSQL_DATABASE')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
