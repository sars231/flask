#! /usr/bin/env python
#coding:utf-8
"""
一个简单的ｆｌａｓｋ程序
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1><center>Hello,World!</center></h1>'

#包含动态路由
@app.route('/user/<username>')
def user(username):
    return '<h1>Hello,myname is %s</h1>' % username

if __name__ == '__main__':
    app.run(debug=True)
