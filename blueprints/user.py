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

bp = Blueprint('user',__name__,url_prefix="/")

@bp.route('/user',methods=['GET','POST'])
def user():

    sql = text('select * from User')
    results = db.session.execute(sql)

    return render_template('user/index.html', results=results)