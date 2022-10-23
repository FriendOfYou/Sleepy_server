import json

from flask import Response, json

from app import app
from app.mysql_data import search_movieDetail, get_Genre, get_Country


@app.route('/movie/<movie_id>/details', methods=['POST', 'GET'])
def detail_movie(movie_id):
    movie = search_movieDetail(movie_id)
    if movie != 0:
        # 将带电影所需体裁获取
        genre = get_Genre(movie_id)
        genres = []
        for i in range(len(genre)):
            genre_data = {'id': genre[i][1], 'name': genre[i][2]}  # 体裁的id和体裁名称
            genres.append(genre_data)
        # 获取电影所属国家/地区信息
        country = get_Country(movie_id)
        countries = []
        for i in range(len(country)):
            country_data = {'id': country[i][1], 'name': country[i][2]}  # 所属国家/地区的id和名称
            countries.append(country_data)

        return Response(json.dumps({'status': 0,
                                    'data': {'id': movie[0], 'name': movie[1], 'year': movie[2], 'rating': movie[3],
                                             'img': movie[5], 'tags': movie[6], 'desc': movie[7],
                                             'genre': genres, 'country': countries}, 'msg': "电影查询成功"}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "错误"}),
                        content_type='application/json')
