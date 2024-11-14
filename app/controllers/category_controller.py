from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user

from app import db
from app.models.category import Category
from app.models.user import User
from app.utils.decorators import admin_required

category_bp = Blueprint('categories', __name__)


@category_bp.route('/categories', methods=['GET'])
@admin_required
@login_required
def category():
    return render_template("category/index.html")


@category_bp.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.all()
    items = [category.to_dict() for category in categories]
    return jsonify(items), 200


@category_bp.route('/api/categories/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200


@category_bp.route('/api/categories', methods=['POST'])
@admin_required
@login_required
def create_category():
    data = request.json
    category_name = data.get('category_name')
    description = data.get('description')

    # Use current_user to get the user_id
    user_id = current_user.id

    category = Category(category_name=category_name, description=description, user_id=user_id)
    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_dict()), 201


@category_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    category.category_name = data.get('category_name', category.category_name)
    category.description = data.get('description', category.description)
    category.user_id = data.get('user_id', category.user_id)

    if not User.query.get(category.user_id):
        return jsonify({'error': 'Invalid user selected.'}), 400

    db.session.commit()
    return jsonify({'message': 'Category updated successfully.'}), 200


@category_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully.'}), 200
