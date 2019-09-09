from flask import render_template,redirect,url_for,flash,request,abort
from . import auth
from ..models import Owner, Asset, Staff, Trip
from .forms import LoginForm,AdminForm,RequestResetForm,PasswordResetForm
from .. import db,mail
from flask_login import login_user,logout_user,login_required,current_user
from ..email import mail_message
from flask_mail import Message
import secrets

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        staff = Staff.query.filter_by(email = login_form.email.data).first()
        if staff is not None and staff.verify_password(login_form.password.data):
            login_user(staff,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('Invalid Username or Password')
    title = "login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/register',methods = ["GET","POST"])
def register():
    # prevent non-admins from accessing the page
    form = AdminForm()
    if form.validate_on_submit():
        staff = Staff(email = form.email.data, name = form.name.data,password = form.password.data,is_admin = True )
        db.session.add(staff)
        db.session.commit()
        # mail_message("Welcome to Sacco-matatu","email/mail",staff.email,staff=staff)

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
