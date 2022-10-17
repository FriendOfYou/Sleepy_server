import json

from flask import request, Response, json, session

from app import app


@app.route('/user/check-token', methods=['POST', 'GET'])
def token_check():
    uid = session.get('uid')
    email = session.get('email')
    name = session.get('name')
    if email is not None:
        return Response(json.dumps({'status': 0, 'user': {'uid': uid, 'name': name, 'email': email}, 'msg': "自动登录"}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'user': None, 'msg': None}), content_type='application/json')
