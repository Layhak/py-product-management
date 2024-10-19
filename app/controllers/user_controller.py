from functools import wraps

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app import db
from app.models.role import Role
from app.models.user import User

user_bp = Blueprint('users', __name__)


def admin_required(f):
    """Decorator to restrict access to admin users only."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'You do not have permission to access this page.'}), 403
        return f(*args, **kwargs)

    return login_required(decorated_function)


@user_bp.route('/api/users', methods=['GET'])
@admin_required
def api_users():
    users = User.query.all()
    items = [user.to_dict() for user in users]
    return jsonify(items), 200


@user_bp.route('/api/users', methods=['POST'])
@admin_required
def api_create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    # Validate role_id to ensure it's a valid role
    if not Role.query.get(role_id):
        return jsonify({'error': 'Invalid role selected.'}), 400

    user = User(name=name, email=email, role_id=role_id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201


@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def api_update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role_id = data.get('role_id', user.role_id)

    # Validate role_id to ensure it's a valid role
    if not Role.query.get(user.role_id):
        return jsonify({'error': 'Invalid role selected.'}), 400

    if 'password' in data and data['password']:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200


@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
