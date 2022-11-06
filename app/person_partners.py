import json

from flask import Response, json

from app import app
from app.mysql_data import search_personPartner, search_personDetail


@app.route('/person/<person_id>/partners', methods=['POST', 'GET'])
def person_partner(person_id):
    data = search_personPartner(person_id)  # 五个合作次数最多的
    if data != 0:
        persons_data = []  # 存放最新的电影数据
        for i in range(len(data)):  # 添加电影数据
            person_data = search_personDetail(data[i][0])
            person = {'times': data[i][1], 'id': person_data[i][0], 'name': person_data[i][1], 'sex': person_data[i][3],
                      'birthday': person_data[i][4], 'birthplace': person_data[i][5], 'summary': person_data[i][6],
                      'img': person_data[i][2]}
            persons_data.append(person)
        return Response(json.dumps({'status': 0, 'msg': "影人相似返回成功", 'list': persons_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "影人相似返回失败"}), content_type='application/json')
