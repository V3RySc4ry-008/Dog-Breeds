import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, AvatarForm

auth_bp = Blueprint('auth', __name__)


def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_avatar(file):
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    return filename


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Войдите в систему.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title='Регистрация')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(next_page or url_for('main.index'))
        flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form, title='Вход')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = AvatarForm()
    if form.validate_on_submit():
        file = form.avatar.data
        if file and file.filename and allowed_file(file.filename):
            if current_user.avatar:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.avatar)
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = save_avatar(file)
            current_user.avatar = filename
            db.session.commit()
            flash('Аватар успешно обновлён!', 'success')
        else:
            flash('Пожалуйста, выберите изображение.', 'warning')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html', form=form, title='Профиль')
