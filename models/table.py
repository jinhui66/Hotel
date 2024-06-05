from exts import db  
from datetime import datetime, timedelta

# 创建模型  
class User(db.Model):  
    __tablename__ = 'User'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    username = db.Column(db.String(15), nullable=False)  # 用户名唯一  
    password = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)  
    
    filepath = db.Column(db.String(255), nullable=True)
    
    # 定义反向关系  
    resume = db.relationship('Resume', backref='user', lazy='dynamic') 
    comment = db.relationship('Comment', backref='user', lazy='dynamic') 
    send_resume = db.relationship('Send_resume', backref='user', lazy='dynamic') 
  
class Resume(db.Model):  
    __tablename__ = 'Resume'    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.String(15), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    expect_position = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    marriage = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.Text(), nullable=True)
    expect_salary = db.Column(db.Integer, nullable=True)
    email = db.Column(db.Text(), nullable=True)
    expect_address = db.Column(db.String(30), nullable=True)
    
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    abilities = db.Column(db.Text, nullable=True)
    about_me = db.Column(db.Text, nullable=True)
        
    filepath = db.Column(db.String(255), nullable=True)  

    # 添加外键列  
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)  
    
class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    username = db.Column(db.String(15), nullable=False)  # 用户名唯一  
    password = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), unique=True, nullable=False)  
    
    filepath = db.Column(db.String(255), nullable=True)
    # 定义反向关系  
    position = db.relationship('Position', backref='admin', lazy='dynamic') 
    
    def to_dict(self):  
        return {"id": self.id, "username": self.username,"email":self.email,"filepath":self.filepath}  

class Position(db.Model):
    __tablename__ = 'Position'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    release_time = db.Column(db.DateTime, nullable=False, default=lambda:datetime.utcnow() + timedelta(hours=8))
    company = db.Column(db.String(300), nullable=False)
    position_name = db.Column(db.String(300), nullable=False)
    salary = db.Column(db.String(150), nullable=False)
    education = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id), nullable=False)
    
    public = db.Column(db.Integer, nullable=False, default=1)
    
    send_resume =db.relationship('Send_resume',backref='position',lazy='dynamic')
    comment = db.relationship('Comment', backref='position', lazy='dynamic')

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=lambda:datetime.utcnow() + timedelta(hours=8))
    
    position_id = db.Column(db.Integer, db.ForeignKey(Position.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id),nullable=False)
    
class EmailCaptcha(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False,default=lambda:datetime.utcnow() + timedelta(hours=8,seconds=300)) 
    
class Send_resume(db.Model):
    __tablename__ = 'send_resume'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    send_time = db.Column(db.DateTime, nullable=False, default=lambda:datetime.utcnow() + timedelta(hours=8))
    name = db.Column(db.String(15), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    expect_position = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    marriage = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.Text(), nullable=True)
    expect_salary = db.Column(db.Integer, nullable=True)
    email = db.Column(db.Text(), nullable=True)
    expect_address = db.Column(db.String(30), nullable=True)
    
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    abilities = db.Column(db.Text, nullable=True)
    about_me = db.Column(db.Text, nullable=True)

    filepath = db.Column(db.String(255), nullable=True)  
    
    status = db.Column(db.String(8), nullable=True)
    
    # 添加外键列  
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)  
    position_id = db.Column(db.Integer, db.ForeignKey(Position.id), nullable=False)
    
    # send_resume_status = db.relationship('Send_resume_status',backref='send_resume',lazy='dynamic')
    
# class Send_resume_status(db.Model):
#     __tablename__ = 'send_resume_status'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
#     send_resume_id = db.Column(db.Integer, db.ForeignKey(Send_resume.id), nullable=False)
    
    
#     a = db.relationship('Send_resume',backref='send_status',lazy='dynamic')
    
# class Accept_resume(db.Model):
#     __tablename__ = 'accept_resume'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
#     send_resume = db.relationship('Send_resume',backref='accept_resume',lazy='dynamic')
#     # 外键
#     send_resume_id =  db.Column(db.Integer, db.ForeignKey(Send_resume.id), nullable=False)  
    
# class Refuse_resume(db.Model):
#     __tablename__ = 'refuse_resume'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
#     send_resume = db.relationship('Send_resume',backref='refuse_resume',lazy='dynamic')
    
#     refuse_resume_id = db.Column(db.Integer, db.ForeignKey(Send_resume.id), nullable=False)  

# class PDFDocument(db.Model):  
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
#     filename = db.Column(db.String(128), nullable=False)  
#     content = db.Column(db.LargeBinary)  # 用于存储PDF文件的二进制内容

