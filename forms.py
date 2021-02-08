from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Length, NumberRange,Email,Optional

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=35)])

    password = PasswordField("password", validators=[InputRequired(), Length(min=6, max=55)])

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=35)])

    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])

    email = StringField("Email", validators=[InputRequired(), Length(max=50)])

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])

    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
class TeamForm(FlaskForm):
    name = StringField("Team Name", validators=[InputRequired(), Length(min=1, max=30)])

    team_image = StringField('(Optional) Team Image URL')
class DeleteForm(FlaskForm):
    """What's up? You want me to delete you we don't have nothing special for that just gonna do it"""

