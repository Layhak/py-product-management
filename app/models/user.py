import binascii
import hashlib
import os

from flask_login import UserMixin

from .. import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))
    image = db.Column(db.String(200))
    password_hash = db.Column(db.String(255))
    password_salt = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', back_populates='users')

    def set_password(self, password):
        salt = os.urandom(32)
        self.password_salt = binascii.hexlify(salt).decode('utf-8')
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password_hash = binascii.hexlify(pwd_hash).decode('utf-8')

    def check_password(self, password):
        salt = binascii.unhexlify(self.password_salt)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return self.password_hash == binascii.hexlify(pwd_hash).decode('utf-8')

    def is_admin(self):
        return self.role.name == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'image': self.image,
            'role': self.role.name if self.role else None
        }

    def __repr__(self):
        return f'<User {self.name}>'
