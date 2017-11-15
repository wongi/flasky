# encoding:utf-8
from flask import Flask,session,redirect,url_for,render_template,flash
# from flask_script import Manager,Shell
from flask_mail import Mail,Message
import os
# from flask_wtf import FlaskForm 
# from wtforms import StringField,SubmitField
# from wtforms.validators import Required
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy 


from config import DevConfig
from models import User,Role




app=Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)
db=SQLAlchemy(app)
app.config.from_object(DevConfig)
# app.config['DEBUG']=True
# app.config['SECRET_KEY']='some thing'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:wj2011go@localhost:3306/hello?charset=utf8mb4'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# app.config['MAIL_SERVER']='smtp.163.com'
# app.config['MAIL_PORT']=465
# app.config['MAIL_USE_SSL']=True
# app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
# app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')

mail=Mail(app)






# class User(db.Model):
# 	__tablename__='users'
# 	id=db.Column(db.Integer,primary_key=True)
# 	username=db.Column(db.String(64),unique=True,index=True)
# 	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

# 	def __repr__(self):
# 		return '<User %r>'% self.username

# class Role(db.Model):
# 	__tablename__='roles'
# 	id=db.Column(db.Integer,primary_key=True)
# 	name=db.Column(db.String(64),unique=True)
# 	users=db.relationship('User',backref='role')

# 	def __repr__(self):
# 		return '<Role %r>'% self.name



# class NameForm(FlaskForm):
# 	name=StringField('what is your name?',validators=[Required()])
# 	sbumit=SubmitField('Submit')

# def send_email(to,subject,template,**kwargs):
# 	msg=Message(subject,sender=os.environ.get('MAIL_USERNAME'),recipients=[to])
# 	msg.body=render_template(template+'.txt',**kwargs)
# 	msg.html=render_template(template+'.html',**kwargs)
# 	mail.send(msg)

# def make_shell_context():
# 	return dict(app=app,db=db,User=User,Role=Role)

# manager.add_command("shell",Shell(make_context=make_shell_context))

@app.route('/',methods=['GET','POST'])
def index():
	form=NameForm()
	if form.validate_on_submit():
		if session.get('name')!=form.name.data:
			flash('Looks like you haved changed your name.')
		user=User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known']=False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'新用户','mail/new_user',user=form.name.data)
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))
	

# if __name__=='__main__':
# 	manager.run()
