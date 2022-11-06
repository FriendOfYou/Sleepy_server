import json

from flask import Response, json

from app import app
from app.mysql_data import search_personLatest, get_Genre, get_Country


@app.route('/person/<person_id>/latest', methods=['POST', 'GET'])
def person_latest(person_id):
    data = search_personLatest(person_id)  # 五个最新的电影数据
    if data != 0:
        movie_data = []  # 存放最新的电影数据
        for i in range(len(data)):  # 添加电影数据
            # 将带电影所需体裁获取
            genre = get_Genre(data[i][0])
            genres = []
            for j in range(len(genre)):
                genre_data = {'id': genre[i][1], 'name': genre[i][2]}  # 体裁的id和体裁名称
                genres.append(genre_data)
            # 获取电影所属国家/地区信息
            country = get_Country(data[i][0])
            countries = []
            for j in range(len(country)):
                country_data = {'id': country[i][1], 'name': country[i][2]}  # 所属国家/地区的id和名称
                countries.append(country_data)
            movie = {'id': data[i][0], 'name': data[i][1], 'year': data[i][2], 'rating': data[i][3], 'img': data[i][5],
                     'tags': data[i][6], 'desc': data[i][7], 'genre': genres, 'country': countries}
            movie_data.append(movie)
        return Response(json.dumps({'status': 0, 'msg': "影人最新5部电影返回成功", 'data': movie_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "影人最新5部电影返回失败"}), content_type='application/json')
