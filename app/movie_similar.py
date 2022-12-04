import json

import json5
from flask import Response, json

from Similar_Recommend import ItemBasedCF
from app import app
from app.mysql_data import get_Genre, get_Country, search_movieSimilar, get_genreCount


# contents = selectUserrate()
# rates = getRatingInfo(contents)
# Item = ItemBasedCF(contents)


@app.route('/movie/<movie_id>/similar', methods=['POST', 'GET'])
def movie_similar(movie_id):
    # count_genre = get_genreCount(movie_id) # 获取该电影的标签数量
    data = search_movieSimilar(movie_id)
    if data != 0:
        movie_data = []
        for i in range(len(data)):  # 添加电影数据
            # 将带电影所需体裁获取
            genre = get_Genre(data[i][0])
            genres = []
            for j in range(len(genre)):
                genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
                genres.append(genre_data)
            # 获取电影所属国家/地区信息
            country = get_Country(data[i][0])
            countries = []
            for j in range(len(country)):
                country_data = {'id': country[j][1], 'name': country[j][2]}  # 所属国家/地区的id和名称
                countries.append(country_data)
            movie = {'id': data[i][0], 'name': data[i][1], 'year': data[i][2], 'rating': data[i][3], 'img': data[i][5],
                     'tags': data[i][6], 'desc': data[i][7], 'genre': genres, 'country': countries}
            movie_data.append(movie)

        return Response(json.dumps({'status': 0, 'msg': "影人最新5部电影返回成功", 'data': movie_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "影人最新5部电影返回失败"}), content_type='application/json')
    # Item.setData('1', movie_id, 5)
    # Item.ItemSimilarity()
    # recommend_dict = Item.Recommend('1', 5, 10)  # k=5, N=10
    # recommend_list = []
    # for k, v in recommend_dict:
    #     recommend_list.append(int(k))
    # movie_data = []
    # for movie_id1 in recommend_list[:10]:
    #     data = search_movieDetail(movie_id1)
    #     count = 0
    #     if data != 0:
    #         genre = get_Genre(movie_id1)
    #         genres = []
    #         for j in range(len(genre)):
    #             genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
    #             genres.append(genre_data)
    #         # 获取电影所属国家/地区信息
    #         country = get_Country(movie_id1)
    #         countries = []
    #         for j in range(len(country)):
    #             country_data = {'id': country[j][1], 'name': country[j][2]}  # 所属国家/地区的id和名称
    #             countries.append(country_data)
    #         movie = {'id': data[0], 'name': data[1], 'year': data[2], 'rating': data[3], 'img': data[5],
    #                  'tags': json5.loads(data[6]), 'desc': data[7], 'genre': genres, 'country': countries}
    #         movie_data.append(movie)
    #         count = count + 1
    #         if count >= 3:
    #             return Response(json.dumps({'status': 0, 'msg': "相似电影返回成功", 'data': movie_data}),
    #                             content_type='application/json')
    # return Response(json.dumps({'status': 1, 'msg': "相似电影返回失败"}), content_type='application/json')

