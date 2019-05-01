# 定义属性配置
import os

# DIALECT = 'mysql'
# DRIVER = 'mysqldb'
# USERNAME = 'root'
# PASSWORD = 'Yaomengjie2'
# HOST = '127.0.0.1'
# PORT = '3306'
# DATEBASE = 'test1'
# SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATEBASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = 'F:\workspace\Pycharm Project\FFD_IMAGE\static\\assets\images'



