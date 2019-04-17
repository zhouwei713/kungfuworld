'''
Created on 20170417

@author: zhou
'''

from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_required, login_user, logout_user, current_user
from app.auth.froms import LoginForm, RegistrationForm, PasswordResetForm, PasswordResetRequestForm
from ..models import User
from .. import db
from ..email import send_email, send_mail
from ..email import send_mail
from werkzeug.utils import redirect
import token


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login/login.html',form=form)


@auth.route('/login-check', methods=['GET', 'POST'])
def login_check():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        # return redirect(url_for('main.index'))
        return "success"
    else:
        # flash('Invalid username or password.')
        return "error"
    # return render_template('login/login.html')


@auth.route('/register-check', methods=['GET', 'POST'])
def register_check():
    email = request.form.get('email1', '')
    password = request.form.get('password1', '')
    name = request.form.get('name1', '')
    user = User.query.filter_by(email=email).first()
    if user is None:
        newuser = User(email=email, username=name, password=password)
        db.session.add(newuser)
        db.session.commit()
        token = newuser.generate_confirmation_token()
        send_email(newuser.email, 'Confirm your Account', 'auth/email/confirm', user=newuser, token=token)
        return "success"
    else:
        return "error"
    # return render_template('login/register.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Account', 'auth/email/confirm',user=user, token=token)
        # send_mail(user.email, 'Confirm your Account', 'auth/email/confirm',user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('login/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/activateaccount')
@login_required
def activate_account():
    return render_template('auth/check_inbox.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    # send_mail(current_user.email, 'Confirm your Account', 'auth/email/confirm',user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('auth.activate_account'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset your password', 'auth/email/reset_password', user=user,
                        token=token,next=request.args.get('next'))
            # send_mail(user.email, 'Reset your password', 'auth/email/reset_password', user=user,
            #            token=token,next=request.args.get('next'))
        flash('An email with instructions to reset your password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
        





    

