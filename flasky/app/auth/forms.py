from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,EqualTo,Regexp,Email
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Password',validators=[Required()])
	remember_me=BooleanField('Keep me loged in')
	submit=SubmitField('Login')

class RegisterForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	username=StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'some wrong')])
	password=PasswordField('Password',validators=[Required(),EqualTo('password2')])
	password2=PasswordField('Confirm Password',validators=[Required()])
	submit=SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('该地址已被注册！')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('该用户名已被注册！')

class ChangePasswordForm(FlaskForm):
	old_password=PasswordField('Old Password',validators=[Required()])
	password=PasswordField('Password',validators=[Required(),EqualTo('password2')])
	password2=PasswordField('Confirm Password',validators=[Required()])
	submit=SubmitField('Update Password')

class ResetForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	submit=SubmitField('Reset Password')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('该地址未注册！')

class ResetPasswordForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Password',validators=[Required(),EqualTo('password2')])
	password2=PasswordField('Confirm Password',validators=[Required()])
	submit=SubmitField('Reset Password')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('该地址未注册！')

class ChangeEmailForm(FlaskForm):
	email=StringField('New Email',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Password',validators=[Required()])
	submit=SubmitField('Change Email')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('该地址已被注册！')

