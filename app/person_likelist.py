import json, json5
from flask import request, Response, json, session

from app import app
from app.mysql_data import search_polikeList, get_Genre, get_Country


@app.route('/person/like/list', methods=['GET'])
def person_likeList():
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
    data = search_polikeList(uid, like)
    if data != 0 and data != -1:
        movies = []
        lengthEnd = page * size
        lengthStart = (page - 1) * size
        if page * size > len(data):
            lengthEnd = len(data)
        for i in range(lengthStart, lengthEnd):
            movie = {'id': data[i][0], 'name': data[i][1], 'sex': data[i][3],
                     'birthday': data[i][4], 'birthplace': data[i][5], 'summary': data[i][6],
                     'img': data[i][2]}
            movies.append(movie)
        total = int(len(data) / size)
        if total * size != len(data):
            total = total + 1
        return Response(json.dumps({'status': 0, 'msg': "影人喜欢/不喜欢列表信息获取成功",
                                    'data': {'page': page, 'total': total, 'nomore': page >= total, 'list': movies}}),
                        content_type='application/json')
    elif data == 0:
        return Response(json.dumps({'status': 0, 'msg': "该用户没有标记影人",
                                    'data': {'nomore':True}}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "标记影人列表信息获取失败",
                                    'data': None}),
                        content_type='application/json')
