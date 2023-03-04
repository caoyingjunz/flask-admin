import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

WORKDIR = "/home/azureuser/flask"
INTERNALIP = "10.0.0.4"


class Config(object):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xas123456@10.0.0.4/xasa?charset=utf8'
