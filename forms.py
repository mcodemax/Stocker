from os import name
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from models import MAX_NAME_LEN, MAX_EMAIL_LEN, MAX_NOTE_LEN, MAX_USERNAME_LEN, MAX_TITLE_LEN

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired(), Length(max=MAX_USERNAME_LEN)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=MAX_NAME_LEN)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=MAX_NAME_LEN)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=MAX_EMAIL_LEN)])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class CreatePortfolioForm(FlaskForm):
    """Form for creating a portfolio"""

    # in progress
    name = StringField('Name your portfolio', validators=[DataRequired(), Length(max=MAX_NAME_LEN)])
    description = StringField('Describe your portfolio (Optional)', validators=[DataRequired(), Length(max=MAX_NOTE_LEN)])