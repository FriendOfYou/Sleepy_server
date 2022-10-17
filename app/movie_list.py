import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_movieList


@app.route('/movie/list', methods=['GET'])
def detail_person():
    page = request.args.get('page')  # 电影所在页的页码；转化为int类型
    if page is not None:
        page = int(request.args.get('page'))
    size = request.args.get('size')  # 每页返回的最大对象数量；转化为int类型
    if size is not None:
        size = int(request.args.get('size'))
    genres = request.args.getlist('genre')  # 电影类型筛选，传入genre的id，一次至多3个;将其转化为int类型
    if genres:
        genres = list(map(int, request.args.getlist('genre')))
    countries = request.args.getlist('country')  # 电影国家筛选，传入country的id，一次至多3个
    if countries:
        countries = list(map(int, request.args.getlist('country')))
    years = request.args.getlist('year')  # 电影年份
    if years:
        years = list(map(int, request.args.getlist('year')))



    data = search_movieList(genres, countries, years)
    Movie = []
    if page * size < len(data):
        for i in range(size * (page - 1), page * size):
            Movie.append(data[i])
    else:
        for i in range(size * (page - 1), len(data)):
            Movie.append(data[i])

    return Response(json.dumps({'status': 0, 'msg': "电影列表信息获取成功", 'data': {'page': page, 'total': len(data)},
                                'list': Movie,
                                }),
                    content_type='application/json')
