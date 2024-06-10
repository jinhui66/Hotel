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

bp = Blueprint('room',__name__,url_prefix="/")

# 添加房间
@bp.route('/create', methods=['GET', 'POST'])
def insert_room():
    if request.method == 'GET':
        return render_template('room/create.html')
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        room_status = request.form.get('room_status')
        roomType_id = request.form.get('roomType_id')

        room_id = int(room_id)
        room_status = int(room_status)
        roomType_id = int(roomType_id)

        # 使用参数化查询来插入数据
        sql = text("INSERT INTO Room VALUES(:room_id, :room_status, :roomType_id)")
        db.session.execute(sql, {'room_id': room_id,'room_status': room_status,'roomType_id': roomType_id})
        db.session.commit()
        #r.exert("insert into Room VALUES(room_id, room_status,roomType_id)")
        return render_template('room/success.html')



# 查看一个房间的具体信息
@bp.route('/query_1', methods=['GET', 'POST'])
def select_room():
    if request.method == 'GET':
        return render_template('room/query_1.html')
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        print(room_id)

        sql = text("SELECT room_status,roomType_id FROM Room WHERE room_id = :room_id")
        result = db.session.execute(sql, {'room_id': room_id}).fetchone()
        print(result)
        # 检查是否找到了结果
        if result:
            room_status = result[0]
            roomType_id = result[1]
        else:
            room_status = None
            roomType_id = None

    return render_template('room/query_1son.html', room_id=room_id, room_status=room_status, roomType_id=roomType_id)


# 删除房间
@bp.route('/delete', methods=['GET', 'POST'])
def delete_room():
    if request.method == 'GET':
        return render_template('room/delete.html')
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        print(room_id)
        sql = text("delete from Room where room_id = :room_id ")
        db.session.execute(sql, {'room_id': room_id})
        db.session.commit()
        return render_template('room/success.html')



@bp.route('/list', methods=['GET', 'POST'])
def select_all():
    if request.method == 'GET':
        sql = text("SELECT * FROM Room")
        data_all = db.session.execute(sql).fetchall()
        # if type(data_all) != 'str':
        #     data_all = str(data_all)
        print(data_all)
        print(len(data_all))
        return render_template('room/list.html', data_all=data_all, data_num=len(data_all))
