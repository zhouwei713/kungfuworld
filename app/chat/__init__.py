'''
Created on 20171025

@author: zhou
'''

from flask import Blueprint

chat = Blueprint('chat', __name__)

from . import views


