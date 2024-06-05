from exts import db
from datetime import datetime, timedelta

# 创建模型
class Vip(db.Model):
    __tablename__ = 'vip'
    vip_level = db.Column(db.Integer, primary_key=True)
    vip_updateRoom = db.Column(db.Integer, nullable=False, default=0, check_constraint='vip_updateRoom IN (0, 1)')
    vip_gift = db.Column(db.Integer, nullable=False, default=0, check_constraint='vip_gift IN (0, 1)')
    vip_discount = db.Column(db.Numeric(2, 1), nullable=False, default=1, check_constraint='vip_discount >= 0 AND vip_discount <= 1')

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_credit = db.Column(db.String(18), nullable=False)
    user_phone = db.Column(db.String(11))
    user_address = db.Column(db.String(50))
    vip_level = db.Column(db.Integer, db.ForeignKey('vip.vip_level'))
    user_password = db.Column(db.String(20))
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'user_credit'),)

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(20), nullable=False)
    admin_phone = db.Column(db.String(11))
    admin_password = db.Column(db.String(20), nullable=False)

class RoomType(db.Model):
    __tablename__ = 'room_type'
    roomType_id = db.Column(db.Integer, primary_key=True)
    roomType_name = db.Column(db.String(20), nullable=False)
    roomType_price = db.Column(db.Numeric(4, 1), nullable=False)

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)
    room_status = db.Column(db.Integer, nullable=False)
    roomType_id = db.Column(db.Integer, db.ForeignKey('room_type.roomType_id'), nullable=False)

class Live(db.Model):
    __tablename__ = 'live'
    live_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=False)
    live_inTime = db.Column(db.Date, nullable=False, default=db.func.current_date())
    live_outTime = db.Column(db.Date)
    is_leaved = db.Column(db.Integer, nullable=False, default=0)

class Bill(db.Model):
    __tablename__ = 'bill'
    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    live_id = db.Column(db.Integer, db.ForeignKey('live.live_id'), nullable=False)
    live_days = db.Column(db.Integer, nullable=False)
    bill_originPrice = db.Column(db.Numeric(6, 1), nullable=False)
    bill_payPrice = db.Column(db.Numeric(6, 1), nullable=False)

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_inTime = db.Column(db.Date, nullable=False)
    book_liveDays = db.Column(db.Integer, nullable=False)
    roomType_id = db.Column(db.Integer, db.ForeignKey('room_type.roomType_id'), nullable=False)
    book_status = db.Column(db.Integer, nullable=False, default=0)

class LivePerson(db.Model):
    __tablename__ = 'live_person'
    livePerson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    livePerson_credit = db.Column(db.String(18), nullable=False)
    livePerson_name = db.Column(db.String(20), nullable=False)
    live_id = db.Column(db.Integer, db.ForeignKey('live.live_id'), nullable=False)
