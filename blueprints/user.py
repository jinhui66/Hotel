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

    sql = text('SELECT * FROM AvailableRooms')
    results = db.session.execute(sql)
    if request.method == 'POST':
        book_inTime = request.form.get('book_inTime')
        book_liveDays = request.form.get('book_liveDays')
        roomType_id = request.form.get('roomType_id')

        print(f"入住时间: {book_inTime}")
        print(f"入住天数: {book_liveDays}")
        print(f"房间类型: {roomType_id}")

        # return redirect(url_for('user.user'))


    return render_template('user/index.html', results=results)

@bp.route('/add_action',methods=['GET','POST'])
def add_action():
    if request.method == 'POST':
        data = request.get_json()
        book_inTime = str(data.get('book_inTime'))
        book_liveDays = str(data.get('book_liveDays'))
        roomType_id = str(data.get('roomType_id'))

        print(f"入住时间: {book_inTime}")
        print(f"入住天数: {book_liveDays}")
        print(f"房间类型: {roomType_id}")

        data = {
            'status': 'success'
        }

    return jsonify(data)
