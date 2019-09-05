from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError
from ..models import Staff

   
class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
class AdminForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    name = StringField('Enter your name',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')
    def validate_email(self,data_field):
        if Staff.query.filter_by(email =data_field.data).first():
            raise ValidationError('There is an account with that email')
    def validate_username(self,data_field):
        if Staff.query.filter_by(name = data_field.data).first():
            raise ValidationError('That name is taken')
            
class RequestResetForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    submit = SubmitField("request password reset")
    
    def validate_email(self,email):
        staff = Staff.query.filter_by(email = email.data).first()
        if staff is None: 
            raise ValidationError('There is no account with that email please register with the administration office') 
        
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('reset password')