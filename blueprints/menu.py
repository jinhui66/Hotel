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

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        pass


@bp.route('/register_action',methods=['GET','POST'])
def register_action():
    if request.method == 'GET':
        return jsonify({'status': '','message':1})

@bp.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')

