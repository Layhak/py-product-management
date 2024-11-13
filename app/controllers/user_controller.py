from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required

from app import db
from app.models.role import Role
from app.models.user import User
from app.utils.decorators import admin_required
from app.utils.file_utils import save_image

user_bp = Blueprint('users', __name__)


@user_bp.route('/api/users/<int:user_id>/upload', methods=['POST'])
def upload_user_image(user_id):
    user = User.query.get_or_404(user_id)
    file = request.files.get('image')

    if not file:
        return jsonify({'error': 'No file provided.'}), 400

    filename = save_image(file, user.name)

    if filename:
        user.image = filename  # Assuming you have an image field
        db.session.commit()
        return jsonify({'message': 'Image uploaded successfully.', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Image upload failed.'}), 400


@user_bp.route('/api/users', methods=['GET'])
@admin_required
def api_users():
    users = User.query.all()
    items = [user.to_dict() for user in users]
    return jsonify(items), 200


@user_bp.route('/api/roles', methods=['GET'])
@admin_required
def api_roles():
    roles = Role.query.all()
    items = [role.to_dict() for role in roles]
    return jsonify(items), 200


@user_bp.route('/users', methods=['GET'])
@admin_required
@login_required
def users():
    return render_template("users/index.html")


@user_bp.route('/api/users', methods=['POST'])
@admin_required
def api_create_user():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')
    gender = data.get('gender')
    role_id = data.get('role_id')
    image = request.files.get('image')

    if not Role.query.get(role_id):
        return jsonify({'error': 'Invalid role selected.'}), 400

    user = User(name=name, email=email, phone=phone, address=address, gender=gender, role_id=role_id)
    user.set_password(password)

    if image:
        filename = save_image(image, user.name)
        user.image = filename

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def api_update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.form  # Use request.form to handle form data
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role_id = data.get('role_id', user.role_id)

    if not Role.query.get(user.role_id):
        return jsonify({'error': 'Invalid role selected.'}), 400

    if 'password' in data and data['password']:
        user.set_password(data['password'])

    file = request.files.get('image')
    if file:
        if user.image:
            user.previous_images.append(user.image)  # Append old image to previous_images
        filename = save_image(file, user.name)
        if filename:
            user.image = filename

    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200


@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
# @token_required
def api_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
