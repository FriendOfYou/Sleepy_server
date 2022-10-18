import json

from flask import request, Response, json

from app import app
from app.mysql_data import search_code, insert_user


@app.route('/user/register', methods=['POST', 'GET'])
def register():
    print(1)
    name = json.dumps(request.form['name'])
    email = json.dumps(request.form['email'])
    code = json.dumps(request.form['code'])
    password = json.dumps(request.form['password'])

    is_value = search_code(email, code)
    if is_value != 0:
        print(111)
        uid = insert_user(name, email, password)
        return Response(json.dumps({'status': 0,
                                    'user': {'uid': uid, 'name': name, 'email': email},
                                    'msg': "注册成功"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'user': None, 'msg': "注册失败"}), content_type='application/json')
