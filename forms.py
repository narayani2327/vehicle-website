from flask_wtf import FlaskForm
import email_validator
from wtforms import validators
from wtforms.fields import StringField,PasswordField,SubmitField,BooleanField,EmailField,IntegerField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class RegistrationForm(FlaskForm):
    # username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    # email=StringField('Email',validators=[DataRequired(),Email()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class OrderForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    phoneNumber=StringField('Phone Number', validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    address=StringField('Address',validators=[DataRequired()])
    number=IntegerField('Number of pieces',validators=[DataRequired()])
    submit=SubmitField('Place Order')

class AdminLogin(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')