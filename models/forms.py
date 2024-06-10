import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from exts import db
from datetime import datetime, timedelta
from sqlalchemy import desc, text
from models.table import User, Admin, EmailCaptcha

# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=10, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证：
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        # user = User.query.filter_by(email=email).first()
        # admin = Admin.query.filter_by(email=email).first()
        sql = text('select * FROM User WHERE email = :email')
        user = db.session.execute(sql, {'email': email}).fetchone()

        sql = text('select * FROM Admin WHERE email = :email')
        admin = db.session.execute(sql, {'email': email}).fetchone()
        print(user)
        print(admin)
        if user or admin:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data

        sql = text('select * from EmailCaptcha where email = :email and captcha = :captcha order by id desc')
        captcha_model = db.session.execute(sql, {'email': email, 'captcha': captcha}).fetchone()
        # captcha_model = EmailCaptcha.query.filter_by(email=email, captcha=captcha).order_by(desc(EmailCaptcha.id)).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        if captcha_model.expiration_time < datetime.utcnow()+timedelta(hours=8):
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        else:
            # todo：可以删掉captcha_model
            # db.session.delete(captcha_model)
            sql = text('delete from EmailCaptcha where id = :id')
            db.session.execute(sql, {'id':captcha_model.id})
            db.session.commit()

class ForgotForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 1. 邮箱是否被注册
    def validate_email(self, field):
        email = field.data
        # get_email = User.query.filter_by(email=email).first()
        # print(1)
        sql = text('select * FROM User WHERE email = :email')
        user = db.session.execute(sql, {'email': email}).fetchone()

        sql = text('select * FROM Admin WHERE email = :email')
        admin = db.session.execute(sql, {'email': email}).fetchone()
        print(user)
        print(admin)
        if not user and not admin:
            raise wtforms.ValidationError(message="该邮箱未被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # captcha_model = EmailCaptcha.query.filter_by(email=email, captcha=captcha).order_by(desc(EmailCaptcha.id)).first()
        sql = text('select * from EmailCaptcha where email = :email and captcha = :captcha order by id desc')
        captcha_model = db.session.execute(sql, {'email': email, 'captcha': captcha}).fetchone()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        if captcha_model.expiration_time < datetime.utcnow()+timedelta(hours=8):
            raise wtforms.ValidationError(message="邮箱或验证码错误！")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

class ChangeForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=10, message="用户名格式错误！")])



