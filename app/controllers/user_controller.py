from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.models.user import User

user_bp = Blueprint('users', __name__)


@user_bp.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


def admin_required(f):
    """Decorator to restrict access to admin users only."""

    def wrap(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return login_required(wrap)


@user_bp.route('/')
@admin_required
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@user_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        user = User(name=name, email=email, role_id=role_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('user.index'))
    return render_template('users/create.html')


@user_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def update(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.role_id = request.form['role_id']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('user.index'))
    return render_template('users/update.html', user=user)


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('user.index'))
