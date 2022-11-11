import json
import json5

from flask import request, Response, json

from app import app
from app.mysql_data import get_Genre, get_Country, search_movie


@app.route('/search/movie', methods=['GET'])
def movie_search():
    word = request.args.get('wd')
    data = search_movie(word)
    if data != 0:
        movies = []
        for i in range(len(data)):
            genre = get_Genre(data[i][0])
            genres1 = []
            for j in range(len(genre)):
                genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
                genres1.append(genre_data)
            country = get_Country(data[i][0])
            countries1 = []
            for k in range(len(country)):
                country_data = {'id': country[k][1], 'name': country[k][2]}  # 所属国家/地区的id和名称
                countries1.append(country_data)
            movie = {'id': data[i][0], 'name': data[i][1], 'year': data[i][2],
                     'rating': data[i][3], 'img': data[i][5], 'tags': json5.loads(data[i][6]),
                     'desc': data[i][7], 'genre': genres1, 'country': countries1}
            movies.append(movie)
        return Response(json.dumps({'status': 0, 'msg': "搜索列表返回成功",
                                    'data': movies}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "搜索列表返回失败",
                                    'data': None}),
                        content_type='application/json')
