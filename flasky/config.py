# encoding:utf-8
import os

class Config(object):
	SECRET_KEY='some string'
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
	MAIL_SERVER='smtp.163.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevConfig(Config):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:wj2011go@localhost:3306/hello?charset=utf8mb4'
	

config={
	'development':DevConfig,
	'default':DevConfig
}