import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import get_movieGenres


@app.route('/movie/genres', methods=['POST', 'GET'])
def movie_genres():
    genre_data = get_movieGenres()
    if genre_data != 0:
        genres = []
        for i in range(len(genre_data)):
            country = {'id': genre_data[i][0], 'name': genre_data[i][1]}
            genres.append(country)
        return Response(json.dumps({'status': 0,
                                    'genres': genres,
                                    'msg': "电影类型传输成功"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'countries': None, 'msg': "电影类型传输失败"}),
                        content_type='application/json')
