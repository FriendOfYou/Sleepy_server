import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_moviePersons


@app.route('/movie/<movie_id>/persons', methods=['POST', 'GET'])
def movie_Person(movie_id):
    data = search_moviePersons(movie_id)
    if data != 0:
        person_data = []
        for i in range(len(data)):
            person = {'role': data[i][0], 'person': {'id': data[i][1], 'name': data[i][2],
                                                     'sex': data[i][3], 'birthday': data[i][4],
                                                     'birthplace': data[i][5],
                                                     'summary': data[i][6], 'img': data[i][7]}}
            person_data.append(person)
        return Response(json.dumps({'status': 0, 'msg': "影人信息查找成功", 'data': person_data}),
                        content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'msg': "影人信息查找失败"}), content_type='application/json')
