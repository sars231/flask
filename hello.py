from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

app = Flask(__name__)
#配置数据库
dasedir = os.path.abspath(os.path.dirname(__file__))

# 设置flask-wtf，设置秘钥
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+os.path.join(dasedir,'date.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)

#定义模型
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


class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('submit')

@app.route('/',methods=['GET','POST'])#加入ＰＯＳＴ方法
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
            #每次提交的名字会和存在会话中的名字进行比较，会话中的名字是前一次在这个表单中提交的数据，如果两个名字不一样，就会调用flash（）函数
        session['name'] = form.name.data   
        return redirect(url_for('index'))#重定向
    return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'))#从回话中读取记录的内容


@app.route('/welcome',methods=['GET','POST'])
def welcome():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data,role_id=3)
            db.session.add(user)#为什么不需要commit，就可以添加到数据表,session.rollback,因为app.config里设置了自动提交
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('welcome'))
    return render_template('welcome.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),known=session.get('known',False))
        

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s</h1>' % name

@app.route('/num/<number>')
def num(number):
    return render_template('num.html',number=number)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


# python shell,在每次运行shell时，都要导入数据库模型和类，为了避免一直这样重复的工作，可以做一些配置，自动导入这些特定的对象
# 为shell注册一个make_context回调函数
def make_shell_context():
    return dict(app=app,db=db,Role=Role,User=User)
manager.add_command('shell',Shell(make_context=make_shell_context))

manager.add_command('db',MigrateCommand)



if __name__ == '__main__':
    manager.run()
