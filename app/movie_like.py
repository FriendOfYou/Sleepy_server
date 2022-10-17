import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import judge_like


@app.route('/movie/<movie_id>/like', methods=['POST', 'GET'])
def movie_like(movie_id):
    like = judge_like(movie_id)
    if like[2] == 1:
        return Response(json.dumps({'status': 0, 'msg': "该用户喜欢该电影", 'data': {'id': like[1], 'like': 1}}),
                        content_type='application/json')
    elif like[2] == -1:
        return Response(json.dumps({'status': 0, 'msg': "该用户不喜欢该电影", 'data': {'id': like[1], 'like': -1}}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "该用户未对该电影评价", 'data': {'id': like[1], 'like': 0}}),
                        content_type='application/json')
