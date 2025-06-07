from collections import Counter
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from .models import User
from . import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def restrict_to_admins():
    if not current_user.is_admin:
        flash('Admins only')
        return redirect(url_for('main.home'))

@admin_bp.route('/')
def dashboard():
    users = User.query.all()
    species_count = Counter(user.species for user in users if user.species)
    return render_template('admin.html', users=users, species_count=species_count)

@admin_bp.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted')
    return redirect(url_for('admin.dashboard'))
