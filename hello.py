from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
# 设置flask-wtf，设置秘钥
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

manager = Manager(app)

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


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s</h1>' % name

@app.route('/num/<number>')
def num(number):
    return render_template('num.html',number=number)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == '__main__':
    manager.run()
