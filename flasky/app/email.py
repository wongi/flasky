from flask import render_template
from flask_mail import Message 
from . import mail 
import os


def send_email(to,subject,template,**kwargs):
	msg=Message(subject,sender=os.environ.get('MAIL_USERNAME'),recipients=[to])
	msg.body=render_template(template+'.txt',**kwargs)
	msg.html=render_template(template+'.html',**kwargs)
	mail.send(msg)
