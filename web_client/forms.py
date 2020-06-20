from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField

class SignUpForm(FlaskForm):
    username = StringField('Penis username')
    password = PasswordField('Penis password')
    submit = SubmitField('Scan your penis')