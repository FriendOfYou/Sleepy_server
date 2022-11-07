import json, json5
from flask import request, Response, json, session

from app import app
from app.mysql_data import search_movieList, get_Genre, get_Country, count_tableLine


@app.route('/movie/list', methods=['GET'])
def movie_list():
    page = request.args.get('page')  # 电影所在页的页码；转化为int类型
    if page is not None:
        page = int(request.args.get('page'))
    size = request.args.get('size')  # 每页返回的最大对象数量；转化为int类型
    if size is not None:
        size = int(request.args.get('size'))
    sortby = request.args.get('sortby')  # 获取的电影的排序顺序，按评分
    genres = request.args.getlist('genre')  # 电影类型筛选，传入genre的id，一次至多3个;将其转化为int类型
    if genres:
        genres = list(map(int, request.args.getlist('genre')))
    countries = request.args.getlist('country')  # 电影国家筛选 传入country的id
    if countries:
        countries = list(map(int, request.args.getlist('country')))
    syear = request.args.getlist('syear')  # 电影筛选开始年份
    if syear is not None:
        syear = int(request.args.get('syear'))
    eyear = request.args.getlist('eyear')  # 电影筛选结束年份
    if eyear is not None:
        eyear = int(request.args.get('eyear'))

    data = search_movieList(genres, countries, syear, eyear, sortby, page, size)
    if data != 0:
        movies = []
        for i in range(len(data)):
            genre = get_Genre(data[i][0])
            genres = []
            for j in range(len(genre)):
                genre_data = {'id': genre[j][1], 'name': genre[j][2]}  # 体裁的id和体裁名称
                genres.append(genre_data)
            country = get_Country(data[i][0])
            countries = []
            for k in range(len(country)):
                country_data = {'id': country[k][1], 'name': country[k][2]}  #  所属国家/地区的id和名称
                countries.append(country_data)
            # data[i][5]=str(data[i][5]).replace('\'', '"')
            movie = {'id': data[i][0], 'name': data[i][1], 'year': data[i][2],
                     'rating': data[i][3], 'img': data[i][5], 'tags': json5.loads(data[i][6]),
                     'desc': data[i][7], 'genre': genres, 'country': countries}
            movies.append(movie)
        total_line = count_tableLine(genres, countries, syear, eyear)
        total = int(len(total_line) / size)
        if total * size != len(data):
            total = total + 1
        return Response(json.dumps({'status': 0, 'msg': "电影列表信息获取成功",
                                    'data': {'page': page, 'total': total, 'list': movies}}),
                        content_type='application/json')

    else:
        return Response(json.dumps({'status': 1, 'msg': "电影列表信息获取失败",
                                    'data': None}),
                        content_type='application/json')
