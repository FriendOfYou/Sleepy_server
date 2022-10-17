import json

from flask import request, Response, json, session

from app import app
from app.mysql_data import search_personDetail, get_movieCountries


@app.route('/movie/countries', methods=['POST', 'GET'])
def movie_countries():
    country_data = get_movieCountries()
    if country_data != 0:
        countries = []
        for i in range(len(country_data)):
            country = {'id': country_data[i][0], 'name': country_data[i][1]}
            countries.append(country)
        return Response(json.dumps({'status': 0,
                                    'countries': countries,
                                    'msg': "国家代码传输成功"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'countries': None, 'msg': "国家代码传输失败"}),
                        content_type='application/json')
