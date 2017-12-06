# encoding:utf-8
from . import auth
from flask_login import login_user,logout_user,login_required,current_user,request
from .forms import LoginForm,RegisterForm,ChangePasswordForm,ResetForm,ResetPasswordForm,ChangeEmailForm
from ..models import User
from flask import render_template,redirect,url_for,flash
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated():
		if not current_user.confirmed and request.endpoint[:5]!='auth.':
			return redirect(url_for('auth.unconfirmed'))

# 注册
@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		user=User(email=form.email.data,username=form.username.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token=user.generate_confirm_token()
		send_email(user.email,'新用户注册','auth/email/confirm',user=user,token=token)
		flash('注册邮件已发出')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

# 确认账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('您已完成账户确认！')
	else:
		flash('链接有误！')
	return redirect(url_for('main.index'))


# 已登录未确认
@auth.route('/unconfirmed')
@login_required
def unconfirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

# 再次发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirm():
	token=current_user.generate_confirm_token()
	send_email(current_user.email,'确认账户','auth/email/confirm',token=token,user=current_user)
	flash('确认邮件已发送')
	return redirect(url_for('main.index'))


# 登录
@auth.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			flash('您已登录账户！')
			return redirect(url_for('main.index'))
		flash('错误的邮件或密码！')
	return render_template('auth/login.html',form=form)

# 登出
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已退出登录！')
	return redirect(url_for('main.index'))


# 修改密码
@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form=ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password=form.password.data
			db.session.add(current_user)
			flash('密码已更新！')
			return redirect(url_for('main.index'))
	return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods=['GET','POST'])
def reset():
	form=ResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user:
			token=user.generate_reset_token()
			send_email(user.email,'密码重置','auth/email/reset',token=token,user=user)
			flash('重置密码确认邮件已发出。')
			return redirect(url_for('main.index'))
	return render_template('auth/reset.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def reset_password(token):
	form=ResetPasswordForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and user.reset_password(token,form.password.data):
			flash('您的密码已重置！')
			return redirect(url_for('auth.login'))
	return render_template('auth/reset.html',form=form)

@auth.route('/change-email',methods=['GET','POST'])
@login_required
def change_email_request():
	form=ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			token=current_user.generate_change_email_token(form.email.data)
			new_email=form.email.data
			send_email(new_email,'更改邮件地址','auth/email/change_email',token=token,user=current_user)
			flash('确认邮件已发出！')
			return redirect(url_for('main.index'))
		else:
			flash('密码错误！')
	return render_template('auth/change_email.html',form=form)

@auth.route('/change-mail/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('邮件地址已更改！')
	else:
		flash('错误的请求！')
	return redirect(url_for('main.index'))

