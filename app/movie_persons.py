import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import  search_moviePersons


@app.route('/movie/<id>/persons', methods=['POST', 'GET'])
def detail_movie(id):
    persons = search_moviePersons(id)
    # if movie != 0:
    #     return Response(json.dumps({'status': 0,
    #                                 'data': {'id': movie[0], 'name': movie[1], 'year': movie[2], 'rating': movie[3],
    #                                          'img': movie[5], 'tags': {'id': 1, 'name': movie[6]}, 'desc': movie[7],
    #                                          'genre': {'id': 1, 'name': movie[8]},
    #                                          'country': {'id': 1, 'name': movie[9]}}}),
    #                     content_type='application/json')
    # else:
    #     return Response(json.dumps({'status': 1, 'data': "错误"}),
    #                     content_type='application/json')
