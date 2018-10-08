'''
Created on 2017415

@author: zhou
'''
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_msearch import Search
from flask_admin import Admin, BaseView, expose
from .aadmin.views import PostView, UserView, RoleView, FollowView

bootstrap = Bootstrap()
moment = Moment()
#manager = Manager(app)
#manager.add_command("runserver", Server(use_debugger=True))
db = SQLAlchemy()
search = Search()
#migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)
mymail = Mail()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from models import User, Post, Role, Follow
admin = Admin(name='Admin Page')
admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(FollowView(Follow, db.session))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    moment.init_app(app)
    mymail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    search.init_app(app)
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    from .chat import  chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    from .aadmin import fadmin as fadmin_blueprint
    app.register_blueprint(fadmin_blueprint)
    #from .RESTful_API_1_0 import API as api_1_0_blueprint
    #app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0/')

    
    return app

