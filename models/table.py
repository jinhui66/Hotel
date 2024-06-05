from exts import db
from datetime import datetime, timedelta

# 创建模型
class Vip(db.Model):
    __tablename__ = 'Vip'
    vip_level = db.Column(db.Integer, primary_key=True)
    vip_updateRoom = db.Column(db.Integer, nullable=False, default=0)
    vip_gift = db.Column(db.Integer, nullable=False, default=0)
    vip_discount = db.Column(db.Numeric(2, 1), nullable=False)

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    user_credit = db.Column(db.String(18))
    user_phone = db.Column(db.String(11))
    user_address = db.Column(db.String(50))
    vip_level = db.Column(db.Integer, db.ForeignKey('Vip.vip_level'), default=1)
    user_password = db.Column(db.String(20), nullable=False)

class Admin(db.Model):
    __tablename__ = 'Admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(25), nullable=False)
    admin_name = db.Column(db.String(20), nullable=False)
    admin_phone = db.Column(db.String(11))
    admin_password = db.Column(db.String(20), nullable=False)

class RoomType(db.Model):
    __tablename__ = 'RoomType'
    roomType_id = db.Column(db.Integer, primary_key=True)
    roomType_name = db.Column(db.String(20), nullable=False)
    roomType_price = db.Column(db.Numeric(4, 1), nullable=False)

class Room(db.Model):
    __tablename__ = 'Room'
    room_id = db.Column(db.Integer, primary_key=True)
    room_status = db.Column(db.Integer, nullable=False)
    roomType_id = db.Column(db.Integer, db.ForeignKey('RoomType.roomType_id'), nullable=False)

class Live(db.Model):
    __tablename__ = 'Live'
    live_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('Room.room_id'), nullable=False)
    live_inTime = db.Column(db.Date, nullable=False, default=db.func.current_date())
    live_outTime = db.Column(db.Date)
    is_leaved = db.Column(db.Integer, nullable=False, default=0)

class Bill(db.Model):
    __tablename__ = 'Bill'
    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    live_id = db.Column(db.Integer, db.ForeignKey('Live.live_id'), nullable=False)
    live_days = db.Column(db.Integer, nullable=False)
    bill_originPrice = db.Column(db.Numeric(6, 1), nullable=False)
    bill_payPrice = db.Column(db.Numeric(6, 1), nullable=False)

class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    book_inTime = db.Column(db.Date, nullable=False)
    book_liveDays = db.Column(db.Integer, nullable=False)
    roomType_id = db.Column(db.Integer, db.ForeignKey('RoomType.roomType_id'), nullable=False)
    book_status = db.Column(db.Integer, nullable=False, default=0)

class LivePerson(db.Model):
    __tablename__ = 'LivePerson'
    livePerson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    livePerson_credit = db.Column(db.String(18), nullable=False)
    livePerson_name = db.Column(db.String(20), nullable=False)
    live_id = db.Column(db.Integer, db.ForeignKey('Live.live_id'), nullable=False)

class EmailCaptcha(db.Model):
    __tablename__ = 'EmailCaptcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False,default=lambda:datetime.utcnow() + timedelta(hours=8,seconds=180))
