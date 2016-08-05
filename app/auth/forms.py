# -*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                            Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


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

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[Required(),
                            EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更改密码')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('新密码', validators=[Required()])
    password2 = PasswordField('确认密码', validators=[Required(), EqualTo('password', message='两次输入必须相同')])
    submit = SubmitField('修改密码')


class ChangeEmailForm(Form):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('修改邮箱')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
