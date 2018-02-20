'''
Created on 20170417

@author: zhou
'''

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
