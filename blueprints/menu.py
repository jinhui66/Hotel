from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from exts import db
import hashlib
import json
from models.forms import RegisterForm,LoginForm,ForgotForm
# from models.table import User, Admin
import os
import time

bp = Blueprint('menu',__name__,url_prefix="/")

@bp.route('/',methods=['GET','POST'])
def menu():
    if not session.get('user_id'):
        return redirect('login')
    elif session['type'] == 'user':
        return render_template('menu/index.html')
    elif session['type'] == 'admin':
        return render_template('room/header.html')


@bp.route('/login',methods=['GET','POST'])
def login():
    return render_template('menu/login.html')


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
                # get_user = User.query.filter_by(email=email).first()
                # 使用原生SQL查询数据
                sql = text('SELECT * FROM User WHERE email = :email')
                get_user = db.session.execute(sql, {'email': email}).fetchone()
                if get_user is not None:
                    session['user_id'] = get_user.user_id
                    session['type'] = 'user'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    print(password)
                    if(get_user.user_password == password):
                        print('success')
                        return jsonify({'status':'success', 'message':''})

            else:
                # get_admin = Admin.query.filter_by(email=email).first()
                sql = text('SELECT * FROM Admin WHERE email = :email')
                get_admin = db.session.execute(sql, {'email': email}).fetchone()
                if get_admin is not None:
                    session['user_id'] = get_admin.admin_id
                    session['type'] = 'admin'
                    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    if(get_admin.admin_password == password):
                        return jsonify({'status': 'success', 'message':''})
        return jsonify({'status':'', 'message':'账号或密码错误'})




@bp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/')

@bp.route('/register',methods=['GET','POST'])
def register():
    return render_template('menu/register.html')

@bp.route('/register_action',methods=['GET','POST'])
def register_action():
    if request.method == 'GET':
        pass
    else:
        type = request.form.get('type')
        form = RegisterForm(request.form)
        print(form.username.data)
        if form.validate():
            email = form.email.data
            username = form.username.data
            print(username)
            password = form.password.data
            if type == 'user':
                # user = User(email=email,user_name=username,user_password=hashlib.sha256(password.encode('utf-8')).hexdigest())
                # # 提交
                # db.session.add(user)
                # db.session.commit()

                sql = text('insert into User(email,user_name,user_password) value(:email, :user_name, :user_password)')
                db.session.execute(sql, {'email': email, 'user_name':username, 'user_password':hashlib.sha256(password.encode('utf-8')).hexdigest()})
                db.session.commit()
                return jsonify({'status': 'success'})
            else: #type == 'admin'
                # admin = Admin(email=email,admin_name=username,admin_password=hashlib.sha256(password.encode('utf-8')).hexdigest())
                # db.session.add(admin)
                # db.session.commit()

                sql = text('insert into Admin(email,admin_name,admin_password) value(:email, :admin_name, :admin_password)')
                db.session.execute(sql, {'email': email, 'admin_name':username, 'admin_password':hashlib.sha256(password.encode('utf-8')).hexdigest()})
                db.session.commit()
                return jsonify({'status': 'success'})
        else:
            for field, errors in form.errors.items():
                # errors 是一个列表，包含该字段的所有错误消息
                if errors:
                #     # 打印第一个错误消息
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")
                    break
                print(error)
            return jsonify({'status': '','message':error})


@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    return render_template('menu/forgot_password.html')

@bp.route('/forgot_password_action',methods=['GET','POST'])
def forgot_password_action():
    if request.method == 'GET':
        pass
    else: # post
        form = ForgotForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            sql_user = text('SELECT * FROM User WHERE email = :email')
            get_user = db.session.execute(sql_user, {'email': email}).fetchone()

            sql_admin = text('SELECT * FROM Admin WHERE email = :email')
            get_admin = db.session.execute(sql_admin, {'email': email}).fetchone()

            if get_user:
                # get_user = User.query.filter_by(email=email).first()
                # get_user.user_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = text('update User set user_password = :user_password where email = :email')
                db.session.execute(sql, {'user_password':hashlib.sha256(password.encode('utf-8')).hexdigest(), 'email': email})
                db.session.commit()
            elif get_admin:
                # get_user = Admin.query.filter_by(email=email).first()
                # get_user.admin_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = text('update Admin set admin_password = :admin_password where email = :email')
                db.session.execute(sql, {'admin_password':hashlib.sha256(password.encode('utf-8')).hexdigest(), 'email': email})
                db.session.commit()

            session.clear()
            return jsonify({'status':'success', 'message':''})
        else:
            for field, errors in form.errors.items():
                # errors 是一个列表，包含该字段的所有错误消息
                if errors:
                #     # 打印第一个错误消息
                    error = errors[0]
                    print(f"{field} 的第一个错误是: {errors[0]}")
                    break
                print(error)
            return jsonify({'status': '','message':error})


