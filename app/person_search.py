import json, json5
from flask import request, Response, json, session

from app import app
from app.mysql_data import search_person


@app.route('/search/person', methods=['GET'])
def person_likeList():
    word = request.args.get('wd')  # 电影所在页的页码；转化为int类型
    data = search_person(word)
    if data != 0:
        persons = []
        for i in range(len(data)):
            person = {'id': data[i][0], 'name': data[i][1], 'sex': data[i][3],
                      'birthday': data[i][4], 'birthplace': data[i][5], 'summary': data[i][6],
                      'img': data[i][2]}
            persons.append(person)
        return Response(json.dumps({'status': 0, 'msg': "影人搜索列表返回成功",
                                    'data': persons}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "影人搜索列表返回失败",
                                    'data': None}),
                        content_type='application/json')
