import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:mysql@localhost:3306/ss20_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
