import datetime

import jwt
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_login import login_user, logout_user, login_required

from app.forms import LoginForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return jsonify({'message': 'Login successful.', 'user': user.to_dict()}), 200
            else:
                return jsonify({'error': 'Invalid email or password.'}), 401
    return render_template('auth/login.html', form=form)


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)

        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Login successful.', 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logout successful.'}), 200
