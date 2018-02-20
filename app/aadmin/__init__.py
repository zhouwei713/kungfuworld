'''
Created on 20180205

@author: zhou
'''

from flask import Blueprint

fadmin = Blueprint('fadmin', __name__)

from . import views
#from ..models import Permission