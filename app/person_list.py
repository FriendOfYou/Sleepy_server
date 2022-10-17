import json

from flask import request, Response, json, session

from app import app


@app.route('/person/list', methods=['POST', 'GET'])
def detail_person():
    print(id)
    # if email is not None:
    #     return Response(json.dumps({'status': 0, 'user': {uid, name, email}, 'msg': "自动登录"}),
    #                     content_type='application/json')
    # else:
    #     return Response(json.dumps({'status': 1, 'user': None, 'msg': None}), content_type='application/json')