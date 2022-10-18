import json

from flask import request, Response, json

from app import app
from app.mysql_data import search_code, insert_user


@app.route('/user/register', methods=['POST', 'GET'])
def register():
    name = json.dumps(request.form['name'])
    email = json.dumps(request.form['email'])
    code = json.dumps(request.form['code'])
    password = json.dumps(request.form['password'])
    # 将从表中读取到的字符串数据两端自带的”去除
    name = name[1:-1]
    email = email[1:-1]
    code = code[1:-1]
    password = password[1:-1]
    is_value = search_code(email, code)
    if is_value != 0:
        uid = insert_user(name, email, password)
        print(uid)
        return Response(json.dumps({'status': 0,
                                    'user': {'uid': uid, 'name': name, 'email': email},
                                    'msg': "注册成功"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'user': None, 'msg': "注册失败"}), content_type='application/json')
