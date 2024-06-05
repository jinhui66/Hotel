from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from exts import db,mail
import hashlib
import json
from models.forms import RegisterForm,LoginForm,ForgotForm
from models.table import User
import os
import time

bp = Blueprint('menu',__name__,url_prefix="/")

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        pass

@bp.route('/login_action',methods=['GET','POST'])
def login_action():
    if request.method == 'GET':
        pass
    else:
        type = request.form.get('type')
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            if type == 'user':
                get_user = User.query.filter_by(email=email).first()
                if get_user is not None:
                    session['user_id'] = get_user.id
                    session['type'] = 'user'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    print(password)
                    if(get_user.password == password):
                        print(1)
                        return jsonify({'status':'success', 'message':''})

            else:
                print('admin')
                get_admin = Admin.query.filter_by(email=email).first()
                if get_admin is not None:
                    session['user_id'] = get_admin.id
                    session['type'] = 'admin'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    if(get_admin.password == password):
                        return jsonify({'status': 'success', 'message':''})
        return jsonify({'status':'', 'message':'账号或密码错误'})

@bp.route('/',methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        return render_template('index.html')
    if request.method == 'GET':
        return render_template('index.html')


@bp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/')
