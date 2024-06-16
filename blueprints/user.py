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

    return render_template('user/index.html', results=results)

# 定义路由，支持GET和POST请求
@bp.route('/add_action',methods=['GET','POST'])
def add_action():
    # 如果是POST请求
    if request.method == 'POST':
        # 从请求体中读取并解析JSON数据，然后从中提取book_inTime、book_liveDays、和roomType_id三个字段
        data = request.get_json()
        book_inTime = str(data.get('book_inTime'))
        book_liveDays = str(data.get('book_liveDays'))
        roomType_id = str(data.get('roomType_id'))

        print(f"入住时间: {book_inTime}")
        print(f"入住天数: {book_liveDays}")
        print(f"房间类型: {roomType_id}")

        # 服务器返回一个JSON响应，表明操作成功
        sqlCommand = text(
            'CALL BookInsertProcedure(:user_id, :book_inTime, :book_liveDays, :roomType_id, @result, @availableRoomId)'
        )
        sqlParams = {
            'user_id': session.get('user_id'),
            'book_inTime': book_inTime,
            'book_liveDays': book_liveDays,
            'roomType_id': roomType_id
        }
        db.session.execute(sqlCommand, sqlParams)
        # 在 SQLAlchemy 中，需要明确地调用 session.commit() 来提交更改。
        db.session.commit()
        results = db.session.execute(text('SELECT @result')).scalar()
        availableRoomId = db.session.execute(text('SELECT @availableRoomId')).scalar()
        returnData = {
            'status': 'success',
            'book_inTime': book_inTime,
            'book_liveDays': book_liveDays,
            'roomType_id': roomType_id,
            'results': results,
            'availableRoomId': availableRoomId
        }

    return jsonify(returnData)
