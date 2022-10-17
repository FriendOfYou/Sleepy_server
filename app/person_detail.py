import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_personDetail


@app.route('/person/<person_id>/details', methods=['POST', 'GET'])
def detail_person(person_id):
    person = search_personDetail(person_id)
    if person != 0:
        return Response(json.dumps({'status': 0,
                                    'data': {'id': person[0], 'name': person[1], 'sex': person[3],
                                             'birthday': person[4],
                                             'birthplace': person[5], 'summary': person[6], 'img': person[2]
                                             },
                                    'msg': "影人信息查询成功"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'data': None, 'msg': "影人查询失败"}),
                        content_type='application/json')