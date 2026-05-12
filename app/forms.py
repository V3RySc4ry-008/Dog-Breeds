from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message='Введите имя пользователя'),
        Length(min=3, max=64, message='Имя должно быть от 3 до 64 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Введите email'),
        Email(message='Введите корректный email')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль'),
        Length(min=6, message='Пароль должен содержать минимум 6 символов')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(message='Подтвердите пароль'),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Этот email уже зарегистрирован.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Введите email'),
        Email(message='Введите корректный email')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль')
    ])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AvatarForm(FlaskForm):
    avatar = FileField('Фото профиля', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Только изображения!')
    ])
    submit = SubmitField('Обновить аватар')
