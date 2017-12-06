from flask_mail import Message
from . import mail
from flask import current_app,render_template

def send_email(to,subject,template,**kw):
	msg=Message(subject,sender=current_app.config['MAIL_USERNAME'],recipients=[to])
	msg.body=render_template(template+'.txt',**kw)
	msg.html=render_template(template+'.html',**kw)
	mail.send(msg)