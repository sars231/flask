from .forms import NameForm
from flask import redirect,render_template,url_for,session,flash,current_app
from datetime import datetime
from . import main
from .. import db
from ..models import User


@main.route('/',methods=['GET','POST'])#加入ＰＯＳＴ方法
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        print('ok')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name')
            #每次提交的名字会和存在会话中的名字进行比较，会话中的名字是前一次在这个表单中提交的数据，如果两个名字不一样，就会调用flash（）函数
        session['name'] = form.name.data   
        return redirect(url_for('.index'))#重定向
    print('no ok')
    return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'))#从回话中读取记录的内容


@main.route('/welcome',methods=['GET','POST'])
def welcome():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data,role_id=3)
            db.session.add(user)#为什么不需要commit，就可以添加到数据表,session.rollback,因为app.config里设置了自动提交
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                print(current_app.config['FLASKY_ADMIN'])
                send_mail(current_app.config['FLASKY_ADMIN'],'New User','new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.welcome'))
    return render_template('welcome.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),known=session.get('known',False))
        

@main.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s</h1>' % name

@main.route('/num/<number>')
def num(number):
    return render_template('num.html',number=number)

