from flask import Blueprint
from flask import Flask,request,render_template,session,redirect,url_for,jsonify
from sqlalchemy import text
from sqlalchemy.exc import StatementError
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
    # if request.method == 'POST':
    #     book_inTime = request.form.get('book_inTime')
    #     book_liveDays = request.form.get('book_liveDays')
    #     roomType_id = request.form.get('roomType_id')

    #     print(f"入住时间: {book_inTime}")
    #     print(f"入住天数: {book_liveDays}")
    #     print(f"房间类型: {roomType_id}")

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
            'CALL BookInsertProcedure(:user_id, :book_inTime, :book_liveDays, :roomType_id, @result1, @availableRoomId)'
        )
        sqlParams = {
            'user_id': session.get('user_id'),
            'book_inTime': book_inTime,
            'book_liveDays': book_liveDays,
            'roomType_id': roomType_id
        }
        try:
            db.session.execute(sqlCommand, sqlParams)
            result1 = db.session.execute(text('SELECT @result1')).scalar()
            availableRoomId = db.session.execute(text('SELECT @availableRoomId')).scalar()
            db.session.commit()

        except StatementError as e:
            print('Error: ' + str(e))
            returnData = {
                'status': 'fail',
                'errorMessage': str(e)
            }
            return jsonify(returnData)
        # 在 SQLAlchemy 中，需要明确地调用 session.commit() 来提交更改。
        print(result1)
        print(availableRoomId)
        returnData = {
            'status': 'success',
            'book_inTime': book_inTime,
            'book_liveDays': book_liveDays,
            'roomType_id': roomType_id,
            'results': result1,
            'availableRoomId': availableRoomId
        }
        return jsonify(returnData)

@bp.route('/queryBook', methods=['GET', 'POST'])
def queryBook():
    sqlCommand = text('SELECT * FROM Book WHERE user_id = :user_id AND book_status = 0 ORDER BY book_inTime')
    sqlParams = {
        'user_id': session.get('user_id')
    }
    sqlResults = db.session.execute(sqlCommand, sqlParams)
    results = []
    for row in sqlResults:
        results.append({
            'book_id': row.book_id,
            'user_id': row.user_id,
            'book_inTime': row.book_inTime.strftime('%Y-%m-%d'),
            'book_liveDays': row.book_liveDays,
            'room_id': row.room_id,
            'book_status': row.book_status
        })

    returnData = {
        'status': 'success',
        'results': results
    }
    return jsonify(returnData)

@bp.route('/addLive', methods = ['GET', 'POST'])
def addLive():
    # 如果是POST请求
    if request.method == 'POST':
        # 从请求体中读取并解析JSON数据，然后从中提取book_inTime、book_liveDays、和roomType_id三个字段
        data = request.get_json()
        book_id = str(data.get('book_id'))
        sqlCommand = text(
            'CALL AddLiveProcedure(:book_id, @result)'
        )
        sqlParams = {
            'book_id': book_id
        }
        db.session.execute(sqlCommand, sqlParams)
        db.session.commit()
        results = db.session.execute(text('SELECT @result')).scalar()
        returnData = {
            'status': 'success',
            'results': results
        }
    return jsonify(returnData)
