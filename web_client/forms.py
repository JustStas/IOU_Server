from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField

class LoadUserForm(FlaskForm):
    username = StringField('Enter username')
#    submit = SubmitField()
