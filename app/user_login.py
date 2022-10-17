import json
import os
from datetime import timedelta
from flask import request, Response, json, session
from app import app
from app.mysql_data import search_user


@app.route('/user/login', methods=['POST', 'GET'])
def login():
    email = json.dumps(request.form['email'])
    password = json.dumps(request.form['password'])
    email = email[1:-1]
    password = password[1:-1]
    print(email)
    print(password)
    print("分割")
    uid = search_user(email, password)
    if uid != 0:
        # app.config['SECRET_KEY'] = os.urandom(24)
        # print(app.config['SECRET_KEY'])
        # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 一天
        session['uid'] = uid[0]
        session['email'] = email  # 将邮箱=email存入Session
        session['name'] = uid[1]
        return Response(
            json.dumps({'status': 0, 'user': {'uid': uid[0], 'name': uid[1], 'email': email}, 'msg': "登录成功"}),
            content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'user': None, 'msg': "登录失败"}), content_type='application/json')
