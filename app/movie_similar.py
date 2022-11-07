import json

import json5
from flask import Response, json

from app import app
from app.mysql_data import search_movieSimilar, get_Genre, get_Country


@app.route('/movie/<movie_id>/similar', methods=['POST', 'GET'])
def movie_similar(movie_id):
    movie = search_movieSimilar(movie_id)  # 三个（至多）相似的电影数据
    if movie != 0:
        movie_data = []  # 存放相似的电影数据
        for i in range(len(movie)):  # 添加电影数据
            # 将带电影所需体裁获取
            genre = get_Genre(movie[i][0])
            genres = []
            for j in range(len(genre)):
                genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
                genres.append(genre_data)
            # 获取电影所属国家/地区信息
            country = get_Country(movie[i][0])
            countries = []
            for j in range(len(country)):
                country_data = {'id': country[j][1], 'name': country[j][2]}  # 所属国家/地区的id和名称
                countries.append(country_data)
            movie = {'id': movie[i][0], 'name': movie[i][1], 'year': movie[i][2], 'rating': movie[i][3],
                     'img': movie[i][5], 'tags': movie[i][6], 'desc': movie[i][7], 'genre': genres,
                     'country': countries}
            movie_data.append(movie)

        return Response(json.dumps({'status': 0, 'msg': "相似电影查询成功",
                                    'data': movie_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "相似查询失败"}),
                        content_type='application/json')
