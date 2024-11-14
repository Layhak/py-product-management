from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user

from app import db
from app.models.category import Category
from app.models.product import Product
from app.utils.decorators import admin_required
from app.utils.file_utils import save_image

product_bp = Blueprint('products', __name__)


@product_bp.route('/products', methods=['GET'])
@admin_required
@login_required
def product():
    return render_template("product/index.html")


@product_bp.route('/api/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    items = [product.to_dict() for product in products]
    return jsonify(items), 200


@product_bp.route('/api/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200


@product_bp.route('/api/products', methods=['POST'])
@admin_required
@login_required
def create_product():
    data = request.form
    product_name = data.get('product_name')
    category_id = data.get('category_id')
    price = data.get('price')
    qty = data.get('qty')
    image = request.files.get('image')

    if not Category.query.get(category_id):
        return jsonify({'error': 'Invalid category selected.'}), 400

    product = Product(
        product_name=product_name,
        category_id=category_id,
        user_id=current_user.id,
        price=float(price),
        qty=int(qty)
    )

    if image:
        filename = save_image(image)
        product.image = filename

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@product_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@admin_required
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.form
    product.product_name = data.get('product_name', product.product_name)
    product.category_id = data.get('category_id', product.category_id)
    product.price = float(data.get('price', product.price))
    product.qty = int(data.get('qty', product.qty))

    if not Category.query.get(product.category_id):
        return jsonify({'error': 'Invalid category selected.'}), 400

    file = request.files.get('image')
    if file:
        if product.image:
            # Optional: Handle previous image cleanup if needed
            pass
        filename = save_image(file)
        if filename:
            product.image = filename

    db.session.commit()
    return jsonify({'message': 'Product updated successfully.'}), 200


@product_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully.'}), 200
