'''
Created on 20171028

@author: zhou
'''

from flask import Blueprint

api = Blueprint('api', __name__)

from . import views, forms

#from ..models import Permission
