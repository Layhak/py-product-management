import datetime

import jwt
from flask import Blueprint, jsonify, request, current_app, render_template, make_response
from flask_login import login_user, logout_user, login_required

from app.models.user import User
from app.validation.auth import LoginForm

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
        login_user(user, remember=True)

        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        response = make_response(jsonify({'message': 'Login successful.', 'token': token}), 200)
        response.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            max_age=60 * 60 * 24 * 7  # 1 week
        )
        return response
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()  # This will handle the Flask-Login session logout

    # Create a response object and clear the token cookie
    response = make_response(jsonify({'message': 'Logout successful.'}))
    response.set_cookie('token', '', expires=0)  # Clear the token cookie by setting its expiration to the past

    return response
