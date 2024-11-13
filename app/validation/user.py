from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    phone = StringField('Phone', validators=[Optional(), Length(min=10, max=15)])
    address = StringField('Address', validators=[Optional(), Length(max=100)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[Optional()])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')
