from flask import Flask,redirect,session,g,send_from_directory
import config
from exts import db,mail
from flask_migrate import Migrate
from blueprints.menu import bp as menu_bp
import os
# import torch

# 启动
app = Flask(__name__)
app.template_folder = 'templates'

# 配置
app.config.from_object(config)

# 默认的静态文件夹仍然是 'static'
app.static_folder = 'static'  # 可以省略

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

# 注册蓝图
app.register_blueprint(menu_bp)

#建表
# with app.app_context():
#     db.create_all()

# @app.before_request
# def my_before_request():
#     user_id = session.get('user_id')
#     type = session.get('type')
#     if user_id and type == 'user':
#         user = User.query.filter_by(id=user_id).first()
#         setattr(g,'user',user)
#         setattr(g,'type','user')
#     elif user_id and type == 'admin':
#         admin = Admin.query.filter_by(id=user_id).first()
#         setattr(g,'user',admin)
#         setattr(g,'type','admin')
#     else:
#         setattr(g,'user',None)
#         setattr(g,'type',None)

#     position_id = session.get('position_id')
#     if position_id:
#         position = Position.query.filter_by(id=position_id).first()
#         setattr(g,'position',position)
#     else:
#         setattr(g,'position',None)

# @app.context_processor
# def my_context_porcessor():
#     return {'user':g.user,'type':g.type}

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')
