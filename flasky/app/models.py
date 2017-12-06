from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String(64),unique=True,index=True)
	username=db.Column(db.String(64),unique=True,index=True)
	password_hash=db.Column(db.String(128))
	confirmed=db.Column(db.Boolean,default=False)
	name=db.Column(db.String(64))
	post_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

	@property
	def password(self):
		raise ValidationError('密码无法访问。')

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def generate_confirm_token(self,experation=3600):
		s=Serializer(current_app.config['SECRET_KEY'],experation)
		return s.dumps({'confirm':self.id})

	def confirm(self,token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('confirm')!=self.id:
			return False 
		self.confirmed=True
		db.session.add(self)
		return True

	def generate_reset_token(self,experation=3600):
		s=Serializer(current_app.config['SECRET_KEY'],experation)
		return s.dumps({'reset':self.id})

	def reset_password(self,token,new_password):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('reset')!=self.id:
			return False
		self.password=new_password
		db.session.add(self)
		return True

	def generate_change_email_token(self,new_email,experation=3600):
		s=Serializer(current_app.config['SECRET_KEY'],experation)
		return s.dumps({'change_email':self.id,'new_email':new_email})

	def change_email(self,token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('change_email')!=self.id:
			return False
		new_email=data.get('new_email')
		if new_email is None:
			return False
		self.email=new_email
		db.session.add(self)
		return True
		
	def __repr__(self):
		return '<User %r>' % self.username

class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='post')

	def __repr__(self):
		return '<Role %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))