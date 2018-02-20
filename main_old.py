'''
Created on 20170326

@author: zhou
'''
from flask import Flask, render_template, app, session, redirect
from flask import request
from flask_bootstrap import Bootstrap
from flask_script import Manager, Server
from flask import url_for, flash
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import backref
import pymysql
from dominate.util import lazy
from flask_migrate import Migrate, MigrateCommand
from __builtin__ import True
from flask_mail import Mail,Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is ZhouLuobo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/zhouluobo'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] ='[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'zwzengyy@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'zwzengyy@gmail.com'
app.config['MAIL_PASSWORD'] = 'zhouwei1203'
app.config['FLASKY_ADMIN'] = 'mowuxue1989@163.com'

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
manager.add_command("runserver", Server(use_debugger=True))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])  
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
    #mail.send(msg)

@app.route("/", methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user',user=user)
                
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known',False),
                           current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/ua')
def useragent():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your User Agent is %s</h1>' % user_agent

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    #db.create_all()
    #app.run(debug=True)
    manager.run()
    
    
    