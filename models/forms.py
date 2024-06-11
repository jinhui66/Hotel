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

        with db.engine.connect() as connection:
            connection.execute(text("CALL is_registered_email(:email, @is_registered);"), {'email':email})
            is_registered = connection.execute(text("SELECT @is_registered;")).fetchone()

            # sql = text('select * FROM User WHERE email = :email')
            # user = db.session.execute(sql, {'email': email}).fetchone()

            # sql = text('select * FROM Admin WHERE email = :email')
            # admin = db.session.execute(sql, {'email': email}).fetchone()
            # print(user)
            # print(admin)
            if is_registered[0] == 1:
                raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data

        with db.engine.connect() as connection:
            # 调用存储过程
            connection.execute(text("CALL is_true_captcha(:email, :captcha, @is_true);"), {'email':email, 'captcha':captcha})
            # 检查会话变量 @is_true
            captcha_model = connection.execute(text("SELECT @is_true;")).fetchone()
            print(captcha_model[0])

            if captcha_model[0] == 0:
                raise wtforms.ValidationError(message="邮箱或验证码错误！")
            connection.commit()

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
        with db.engine.connect() as connection:
            connection.execute(text("CALL is_registered_email(:email, @is_registered);"), {'email':email})
            is_registered = connection.execute(text("SELECT @is_registered;")).fetchone()

            # sql = text('select * FROM User WHERE email = :email')
            # user = db.session.execute(sql, {'email': email}).fetchone()

            # sql = text('select * FROM Admin WHERE email = :email')
            # admin = db.session.execute(sql, {'email': email}).fetchone()
            # print(user)
            # print(admin)
            if is_registered[0] == 0:
                raise wtforms.ValidationError(message="该邮箱未被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data

        with db.engine.connect() as connection:
             # 调用存储过程
            connection.execute(text("CALL is_true_captcha(:email, :captcha, @is_true);"), {'email':email, 'captcha':captcha})
            # 检查会话变量 @is_true
            captcha_model = connection.execute(text("SELECT @is_true;")).fetchone()
            print(captcha_model[0])

            if captcha_model[0] == 0:
                raise wtforms.ValidationError(message="邮箱或验证码错误！")
            connection.commit()



class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

class ChangeForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=10, message="用户名格式错误！")])



