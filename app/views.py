import os
import hmac
import hashlib
from urllib.parse import urlencode

from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import User
from .forms import RegistrationForm, LoginForm, EditProfileForm
from .config import Config

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@bp.route('/telegram_login')
def telegram_login():
    data = request.args.to_dict()
    if verify_telegram_login(data):
        telegram_id = data.get('id')
        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id,
                        name=data.get('first_name'),
                        email=f"{data.get('username')}@telegram")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    flash('Telegram login failed')
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return redirect(url_for('main.register'))
        user = User(email=form.email.data, name=form.name.data, species=form.species.data, bio=form.bio.data)
        user.set_password(form.password.data)
        if form.photo.data:
            filename = save_photo(form.photo.data)
            user.photo = filename
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.species = form.species.data
        current_user.bio = form.bio.data
        if form.photo.data:
            filename = save_photo(form.photo.data)
            current_user.photo = filename
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('main.home'))
    return render_template('edit_profile.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


def verify_telegram_login(data: dict) -> bool:
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        return False
    received_hash = data.pop('hash', None)
    if not received_hash:
        return False
    check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(token.encode()).digest()
    h = hmac.new(secret_key, msg=check_string.encode(), digestmod=hashlib.sha256)
    return h.hexdigest() == received_hash

def save_photo(file_storage):
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    filename = secure_filename(file_storage.filename)
    path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file_storage.save(path)
    return filename
