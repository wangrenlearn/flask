# -*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                            Email()])
    username = StringField('用户名', validators=[Required(), Length(1,64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    'Usernames must have only letters, '
                                                    'numbers, dots or underscores')])
    password = PasswordField('密码', validators=[Required(),
                            EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def Validate_username(self, field):
        if User.quiry.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                            Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('密码', validators=[Required(),
                            EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更改密码')

