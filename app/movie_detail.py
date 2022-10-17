import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_movieDetail


@app.route('/movie/<movie_id>/details', methods=['POST', 'GET'])
def detail_movie(movie_id):
    movie = search_movieDetail(movie_id)
    if movie != 0:
        return Response(json.dumps({'status': 0,
                                    'data': {'id': movie[0], 'name': movie[1], 'year': movie[2], 'rating': movie[3],
                                             'img': movie[5], 'tags': {'id': 1, 'name': movie[6]}, 'desc': movie[7],
                                             'genre': {'id': 1, 'name': movie[8]},
                                             'country': {'id': 1, 'name': movie[9]}}, 'msg':"电影查询成功"}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "错误"}),
                        content_type='application/json')
