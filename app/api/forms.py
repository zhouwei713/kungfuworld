'''
Created on 20171029

@author: zhou
'''

from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField,BooleanField, SelectField, FileField
from wtforms.validators import Required, EqualTo, Length, Regexp, Email, DataRequired
from flask_wtf import Form
from werkzeug.routing import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField
from wtforms.validators import Regexp

class QueryIPForm(Form):
    search = StringField('Search for IP', validators=[DataRequired(),
                                                      Regexp('^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$',0,"Invalid IP")])
    submit = SubmitField('Query It')
    #submit2 = SubmitField('Check IP Detail')

class TalkForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
