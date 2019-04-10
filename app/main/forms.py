'''
Created on 2017415

@author: zhou
'''
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField, \
    BooleanField, SelectField, FileField
from wtforms.validators import Required, EqualTo, Length, Regexp, Email, DataRequired
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChangePw(FlaskForm):
    oldpassword = PasswordField('Enter Your Old Password', validators=[DataRequired()])
    newpassword = PasswordField('Enter Your New Password', validators=[DataRequired(), EqualTo('newpassword2',
                                                                                    message='Passwords must match')])
    newpassword2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Go')


class EditProfileForm(FlaskForm):
    # avatar = FileField('Profile Picture')
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About ma')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    'Username must have only letters, numbers, dots or underscores')]
                           )
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('User already in use.')


class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    'Username must have only letters, numbers, dots or underscores')]
                           )
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    postname = StringField("Post Name", validators=[DataRequired()])
    noveLname = StringField('Novel Name', validators=[DataRequired()])
    body = PageDownField("Post Your Novel?", validators=[DataRequired()])
    picture = StringField("Upload Your Picture")
    original = StringField("Original Author")
    tag = StringField("Tag")
    voice = StringField("voice")
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = PageDownField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
