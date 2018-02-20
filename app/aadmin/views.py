'''
Created on 20180205

@author: zhou
'''

from flask import Flask
from flask_login import current_user
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
#from ..decorators import admin_required
from flask_login import login_required
#from ..models import User

class DBView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator()

    @expose('/')
    def index(self):
        return self.render('aadmin/index.html')

class UserView(ModelView):
    # Override displayed fields
    #column_list = ('login', 'email')
    def is_accessible(self):
        return current_user.is_administrator() and current_user.is_authenticated

    def __init__(self, User ,session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

class PostView(ModelView):
    # Override displayed fields
    #column_list = ('login', 'email')
    def is_accessible(self):
        return current_user.is_administrator()

    def __init__(self, Post ,session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PostView, self).__init__(Post, session, **kwargs)

class RoleView(ModelView):
    # Override displayed fields
    #column_list = ('login', 'email')
    def is_accessible(self):
        return current_user.is_administrator()

    def __init__(self, Role ,session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RoleView, self).__init__(Role, session, **kwargs)

class FollowView(ModelView):
    # Override displayed fields
    #column_list = ('login', 'email')
    def is_accessible(self):
        return current_user.is_administrator()

    def __init__(self, Follow ,session, **kwargs):
        # You can pass name and other parameters if you want to
        super(FollowView, self).__init__(Follow, session, **kwargs)




