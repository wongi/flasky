class Config:
	SECRET_KEY='some string'
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True

	MAIL_SERVER='smtp.163.com'
	MAIL_PORT=465
	MAIL_USE_SSL=True
	MAIL_USERNAME='bintas@163.com'
	MAIL_PASSWORD='wj2011go'
	MAIL_ADMIN='wongi@foxmail.com'

	@staticmethod
	def init_app(app):
		pass 

class DevConfig(Config):
	DEBUG=True
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:wj2011go@localhost:3306/flasky?charset=utf8mb4'

config={
	'development':DevConfig,
	'default':DevConfig
}