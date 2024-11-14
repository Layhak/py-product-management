from app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200))  # Assuming this stores the path to the image

    # Define relationships
    category = db.relationship('Category', back_populates='products')
    user = db.relationship('User', back_populates='products')

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'price': self.price,
            'qty': self.qty,
            'image': self.image
        }

    def __repr__(self):
        return f'<Product {self.product_name}>'
