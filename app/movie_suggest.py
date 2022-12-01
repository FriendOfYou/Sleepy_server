import json

import json5
from flask import Response, json, session

from app import app
from app.mysql_data import get_Genre, get_Country, selectUserrate, search_molikeList, search_movieDetail
import RecommendAnalysis

data = {}


def FilCompareData():
    user_rate = selectUserrate()
    for i in range(len(user_rate)):
        if not user_rate[i][0] in data.keys():
            data[user_rate[i][0]] = {user_rate[i][1]: user_rate[i][2]}
        else:
            data[user_rate[i][0]][user_rate[i][1]] = user_rate[i][2]


FilCompareData()


@app.route('/suggest', methods=['POST', 'GET'])
def movie_suggest():
    # 对用户登陆状态进行检查
    uid = session.get('uid')  # 从session读取用户uid
    if uid is None:
        return Response(json.dumps({'status': 1, 'msg': "用户未登录"}),
                        content_type='application/json')
    movie_like = search_molikeList(uid, 1)  # 获取用户喜欢的电影信息
    if len(movie_like) < 5:
        return Response(json.dumps({'status': 1, 'msg': "用户喜欢电影数量过少"}), content_type='application/json')
    for i in range(len(movie_like)):
        if not movie_like[i][0] in data.keys():
            data[uid] = {movie_like[i][1]: 5}
        else:
            data[uid][movie_like[i][1]] = 5
    Recommendations = RecommendAnalysis.recommend(uid, data)
    if Recommendations:
        movie_data = []
        for i in range(len(Recommendations)):  # 添加电影数据
            movie = search_movieDetail(Recommendations[i][0])
            # 将带电影所需体裁获取
            genre = get_Genre(Recommendations[i][0])
            genres = []
            for j in range(len(genre)):
                genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
                genres.append(genre_data)
            # 获取电影所属国家/地区信息
            country = get_Country(Recommendations[i][0])
            countries = []
            for j in range(len(country)):
                country_data = {'id': country[j][1], 'name': country[j][2]}  # 所属国家/地区的id和名称
                countries.append(country_data)
            movie_one = {'id': movie[i][0], 'name': movie[i][1], 'year': movie[i][2], 'rating': movie[i][3],
                         'img': movie[i][5],
                         'tags': json5.loads(movie[6]), 'desc': movie[i][7], 'genre': genres, 'country': countries}
            movie_data.append(movie_one)
        return Response(json.dumps({'status': 0, 'msg': "返回成功", 'data': movie_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "返回失败"}), content_type='application/json')
