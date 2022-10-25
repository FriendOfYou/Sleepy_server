import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import judge_Movielike, set_Movielike, update_Movielike


@app.route('/movie/<movie_id>/like', methods=['POST', 'GET'])
def movie_like(movie_id):
    # 对用户登陆状态进行检查
    uid = session.get('uid')  # 从session读取用户uid
    if uid is None:
        return Response(json.dumps({'status': 1, 'msg': "用户未登录"}),
                        content_type='application/json')
    # 查询电影标记喜欢/不喜欢
    if request.method == 'GET':
        like = judge_Movielike(movie_id, uid)
        if like != 0:
            if like[2] == 1:
                return Response(json.dumps({'status': 0, 'msg': "该用户喜欢该电影", 'like': 1}),
                                content_type='application/json')
            elif like[2] == -1:
                return Response(json.dumps({'status': 0, 'msg': "该用户不喜欢该电影", 'like': -1}),
                                content_type='application/json')
            else:
                return Response(json.dumps({'status': 0, 'msg': "该用户未对该电影评价", 'like': 0}),
                                content_type='application/json')
        else:
            set_Movielike(movie_id, uid)
            return Response(json.dumps({'status': 0, 'msg': "该用户未对该电影评价", 'like': 0}),
                            content_type='application/json')
    # 设置电影标记喜欢/不喜欢
    else:
        like_choice = request.get_data()  # 读取用户对电影的评价
        # like_choice = like_choice.decode('utf-8')  # 将读取的字节数据转化为utf-8字符
        like_choice = json.loads(like_choice)['like']  # 读取实际评价选项数值 1：喜欢 -1：不喜欢 0：未评价
        if update_Movielike(movie_id, uid, like_choice) == 1:
            return Response(json.dumps({'status': 0, 'msg': "电影标记成功"}),
                            content_type='application/json')
        else:
            return Response(json.dumps({'status': 1, 'msg': "电影标记失败"}),
                            content_type='application/json')
