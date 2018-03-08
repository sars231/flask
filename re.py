#! /usr/bin/env python
#coding:utf8
"""
请求与响应
"""


from flask import Flask,requests

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = requests.headers.get('User-Agent')
    host = requests.headers.get('Host')
    cookie = requests.headers.get('Cookie')
    return '<h2>your browser is %s</h2></br><h2>your Host is %s</h2></br><p>Cookie:%s</p>' % (user_agent,host,cookie)

if __name__ == '__main__':
    app.run(debug=True)
