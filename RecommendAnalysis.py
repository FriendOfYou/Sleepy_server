from math import *


def Euclidean(user1, user2, data):
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))


def top_simliar(userID, data):
    res = []
    for userid in data.keys():
        # 排除与自己计算相似度
        if not userid == userID:
            simliar = Euclidean(userID, userid, data)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]


def recommend(user, data):
    top_sim_user = top_simliar(user, data)[0][0]
    items = data[top_sim_user]
    recommendations = []
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    return recommendations[:10]

# Recommendations = recommend(5)
# print("为用户推荐下列影片")
# for video in Recommendations:
#     print(video[0])
