from flask import Flask,render_template
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

manager = Manager(app)


@app.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())


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
