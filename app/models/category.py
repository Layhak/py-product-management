from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='categories')
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'description': self.description,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Category {self.category_name}>'
