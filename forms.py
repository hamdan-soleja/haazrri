from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,RadioField
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)])
    role = RadioField("Select an option:",
                        choices=[("1", "Student"), ("2", "Teacher")],
                        coerce=str)
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

class AttendanceForm(FlaskForm):
    username = StringField('Attendance Code', validators=[InputRequired()])
    roll_number = StringField('Roll Number', validators=[InputRequired()])
    submit = SubmitField('Submit')
