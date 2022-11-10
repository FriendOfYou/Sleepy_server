import json, json5
from flask import request, Response, json, session

from app import app
from app.mysql_data import search_molikeList, get_Genre, get_Country


@app.route('/movie/like/list', methods=['GET'])
def movie_likeList():
    # 对用户登陆状态进行检查
    uid = session.get('uid')  # 从session读取用户uid
    if uid is None:
        return Response(json.dumps({'status': 1, 'msg': "用户未登录"}),
                        content_type='application/json')
    page = request.args.get('page')  # 电影所在页的页码；转化为int类型
    if page is not None:
        page = int(request.args.get('page'))
    size = request.args.get('size')  # 每页返回的最大对象数量；转化为int类型
    if size is not None:
        size = int(request.args.get('size'))
    like = request.args.get('like')  # 电影筛选开始年份
    if like is not None:
        like = int(request.args.get('like'))
    if like != 1 and like != -1:
        return Response(json.dumps({'status': 1, 'msg': "喜欢或不喜欢的标记出错",
                                    'data': None}),
                        content_type='application/json')
    data = search_molikeList(uid, like)
    if data != -1 and data != 0:
        movies = []
        lengthEnd = page * size
        lengthStart = (page - 1) * size
        if page * size > len(data):
            lengthEnd = len(data)
        for i in range(lengthStart, lengthEnd):
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
        total = int(len(data) / size)
        if total * size != len(data):
            total = total + 1
        return Response(json.dumps({'status': 0, 'msg': "电影喜欢/不喜欢列表信息获取成功",
                                    'data': {'page': page, 'total': total, 'list': movies}}),
                        content_type='application/json')
    elif data == 0:
        return Response(json.dumps({'status': 0, 'msg': "该用户没有喜欢或不喜欢的电影",
                                    'data': None}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "电影列表信息获取失败",
                                    'data': None}),
                        content_type='application/json')
