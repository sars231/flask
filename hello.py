#! /usr/bin/env python
<<<<<<< HEAD
#coding utf-8
=======
#coding:utf-8
"""
一个简单的ｆｌａｓｋ程序
"""
>>>>>>> 9b6facd752848bb986dd8020634bbd948c5faab9

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1><center>Hello,World!</center></h1>'

<<<<<<< HEAD
=======
#包含动态路由
@app.route('/user/<username>')
def user(username):
    return '<h1>Hello,myname is %s</h1>' % username

>>>>>>> 9b6facd752848bb986dd8020634bbd948c5faab9
if __name__ == '__main__':
    app.run(debug=True)
