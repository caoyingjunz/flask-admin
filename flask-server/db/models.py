from db.interface import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))
    email = db.Column(db.String(256))
    description = db.Column(db.String(1024))

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    status = db.Column(db.String(16)) # 0: 未开始 1: 进行中 2: 完成  3: 失败
    progress = db.Column(db.String(128))
    create_at = db.Column(db.String(128))
    owner = db.Column(db.String(256))
