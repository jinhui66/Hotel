# flask
数据库课程设计期末作业，酒店管理系统。

**config.py**文件需要自行配置。

conda环境在**environment.yaml**中。

## conda环境导入:
```
conda env create --file environment.yaml
```

## config.py
```
# 自己进行配置
SECRET_KEY = '123456'
# 数据库的配置信息
HOSTNAME = ""
PORT = 3306
USERNAME = ""
PASSWORD = ""
DATABASE = ""
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USER_SSL = True
MAIL_PORT = 587
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = ""

```
