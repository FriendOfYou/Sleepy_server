import json

from flask import Response, json

from TextAnalysis import TextAnalysis
from app import app
from app.mysql_data import selectComment


@app.route('/movie/<movie_id>/comments', methods=['POST', 'GET'])
def comment_movie(movie_id):
    comment_data = selectComment(movie_id)
    if comment_data != 0 and len(comment_data) != 0:
        good = []
        bad = []
        for i in range(len(comment_data)):
            text = comment_data[i][1]
            s = TextAnalysis(text=text)
            good_bad = s.positivity()
            if good_bad['negative_num'] < good_bad['positive_num']:
                good.append(
                    {'comment': comment_data[i][1], 'readability': s.readability(),
                     'valence': s.sentiment_by_valence()['valence']})
            elif good_bad['negative_num'] > good_bad['positive_num']:
                bad.append(
                    {'comment': comment_data[i][1], 'readability': s.readability(),
                     'valence': s.sentiment_by_valence()['valence']})
        good.sort(key=lambda x: x['readability'])
        bad.sort(key=lambda x: x['readability'])
        good = good[:3]
        bad = bad[:3]
        positive = []
        negative = []
        for i in range(len(good)):
            positive.append(
                {'movie_id': comment_data[0][2], 'text': good[i]['comment'], 'readability': good[i]['readability'],
                 'valence': good[i]['valence']})
            negative.append(
                {'movie_id': comment_data[0][2], 'text': bad[i]['comment'], 'readability': bad[i]['readability'],
                 'valence': bad[i]['valence']})
        return Response(json.dumps({'status': 0,
                                    'data': {'positive': positive, 'negative': negative},
                                    'msg': "评论返回成功"}), content_type='application/json')
    elif len(comment_data) == 0:
        return Response(json.dumps({'status': 0,
                                    'data': None,
                                    'msg': "评论条数空"}), content_type='application/json')
    else:
        return Response(json.dumps({'status': 1, 'data': None, 'msg': "评论返回失败"}),
                        content_type='application/json')
