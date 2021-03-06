from . import db
from werkzeug.security import generate_password_hash,check_password_hash
#使用Ｗｅｒｋｚｅｕｇ实现密码散列


class Role(db.Model):
    __tablename__ = 'roles'#定义表名称
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))#设置外键
    def __repr__(self):
        return '<User %r>' % self.username
    
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise ArithmeticError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
