# -*- coding=utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from ..email import send_email
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm, PasswordResetRequestForm, PasswordResetForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码不正确！')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出。')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('认证邮件已发送到你的邮箱。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账户已确认，谢谢！')
    else:
        flash('认证链接不正确或已过期。')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
            'auth/email/confirm', user=current_user, token=token)
    flash('新的认证邮件已发送到你的邮箱。')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['POST','GET'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('密码已修改.')
            return redirect(url_for('main.index'))
        else:
            flash('密码不正确！')
    return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_confirmation_token()
            send_email(user.email, '重设密码',\
                    'auth/email/reset_password',\
                    user=user, token=token,\
                    next=request.args.get('next'))
            flash('重置密码的邮件已发送到你的邮箱。')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('密码已更改.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_confirmation_token(new_email)
            send_email(new_email, '确认你的邮箱地址' \
                    'auth/email/change_email', \
                    user=current_user, token=token)
            flash('用于更改并确认新邮箱的邮件已发送至你的新邮箱。')
            return redirect(url_for('main.index'))
        else:
            flash('邮箱或密码不正确。')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('邮箱已更改。')
    else:
        flash('请求失败。')
    return redirect(url_for('main.index'))
