import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_personList, search_personlength


@app.route('/person/list', methods=['POST', 'GET'])
def list_person():
    page = request.args.get('page')  # 电影所在页的页码；转化为int类型
    if page is not None:
        page = int(request.args.get('page'))
    size = request.args.get('size')  # 每页返回的最大对象数量；转化为int类型
    if size is not None:
        size = int(request.args.get('size'))
    person_data = search_personList(page, size)
    data = search_personlength()
    if person_data != 0:
        persons = []
        for i in range(len(person_data)):
            person = {'id': person_data[i][0], 'name': person_data[i][1], 'sex': person_data[i][3],
                      'birthday': person_data[i][4], 'birthplace': person_data[i][5], 'summary': person_data[i][6],
                      'img': person_data[i][2]}
            persons.append(person)
        total = int(int(data[0]) / size)
        if total * size != int(data[0]):
            total = total + 1
        return Response(
            json.dumps({'status': 0, 'msg': "影人列表信息获取成功", 'data': {'page': page, 'total': total, 'list': persons}
                        }),
            content_type='application/json')
    else:
        return Response(
            json.dumps({'status': 1, 'msg': "影人列表信息获取失败", 'data': None}), content_type='application/json')
