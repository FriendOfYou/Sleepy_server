import json

from flask import Response, json, session

from app import app
from app.mysql_data import search_molikeList, search_movieTags


@app.route('/suggest/wordcloud', methods=['POST', 'GET'])
def movie_wordCloud():
    # 对用户登陆状态进行检查
    uid = session.get('uid')  # 从session读取用户uid
    if uid is None:
        return Response(json.dumps({'status': 1, 'msg': "用户未登录"}),
                        content_type='application/json')
    data = search_molikeList(uid, 1)  # 获取用户喜欢的电影信息
    if data != 0:
        if len(data) < 5:  # 用户至少应有五部电影
            return Response(json.dumps({'status': 1, 'msg': "用户喜欢电影数过少"}), content_type='application/json')
        movie_data = []
        tags = {}
        for i in range(len(data)):  # 添加电影数据
            movie_tag = search_movieTags(data[i][0])  # 获取电影id和电影的标签tags
            tag = str(movie_tag[1][1:-1])
            tag = tag.split(',')
            for j in range(len(tag)):
                if not tag[j][1:-1] in data.keys():  # tag[j][1:-1]表示第j个标签的具体内容，[1:-1]的目的是去除标签两端的‘’
                    tags[tag[j][1:-1]] = {'tag_name': tag[j][1:-1], 'tag_count': 1, 'movie_example': data[i][0]}
                else:
                    tags[tag[j][1:-1]]['tag_count'] = tags[tag[j][1:-1]]['tag_count'] + 1
        for key in tags.keys():
            movie_tags = {'name': tags[key]['tag_name'], 'value': tags[key]['tag_count'],
                          'mid': tags[key]['movie_example']}
            movie_data.append(movie_tags)
        return Response(json.dumps({'status': 0, 'msg': "用户词云信息返回成功", 'data': movie_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "用户词云返回失败返回失败"}), content_type='application/json')
