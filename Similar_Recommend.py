import math


class ItemBasedCF:
    def __init__(self, train_file):
        self.train = dict()
        self.train_file = train_file
        self.readData()

    def readData(self):
        for i in range(len(self.train_file)):
            user = self.train_file[i][0]
            item = self.train_file[i][1]
            score = self.train_file[i][1]
            self.train.setdefault(user, {})
            self.train[user][item] = int(float(score))

    def setData(self, user, item, score):
        self.train.setdefault(user, {})
        self.train[user][item] = int(float(score))

    def ItemSimilarity(self):
        N = dict()  # 物品被多少个不同用户购买
        C = dict()  # 物品和物品的共现矩阵
        for user, items in self.train.items():
            for ikey in items.keys():  # ikey: {'a': 1, 'b': 1, 'd': 1}
                # print('ikey:', ikey)
                N.setdefault(ikey, 0)
                N[ikey] += 1

                C.setdefault(ikey, {})
                for jkey in items.keys():  # 物品和物品的共现矩阵 jkey: {'a': 1, 'b': 1, 'd': 1}
                    if ikey == jkey:
                        continue
                    # print('jkey:', jkey)
                    C[ikey].setdefault(jkey, 0)
                    # C[ikey][jkey] += 1
                    C[ikey][jkey] += 1 / math.log(1 + len(items) * 1.0)  # 用用户活跃度来修正相似度，len(items)来衡量用户活跃度

        # 根据N，C计算物品之间的相似度
        # 根据C得到物品和物品共现的次数，根据N得到物品分别出现的次数
        self.W = dict()
        self.W_max = dict()  # 记录每一列的最大值
        for ikey, relateij in C.items():
            # print('ikey:', ikey)
            # print('relateij:', relateij)
            self.W.setdefault(ikey, {})
            for jkey, Wij in relateij.items():
                self.W_max.setdefault(jkey, 0.0)  # 初始化当列最大值为0
                self.W[ikey][jkey] = Wij / (math.sqrt(N[ikey] * N[jkey]))  # 计算相似度
                if self.W[ikey][jkey] > self.W_max[jkey]:
                    self.W_max[jkey] = self.W[ikey][jkey]  # 更新列中最大值
                    # print('jkey:', jkey, 'self.W_max:', self.W_max[jkey])

        # 归一化处理, Wij / Wij_max
        for ikey, relateij in C.items():
            for jkey, Wij in relateij.items():
                self.W[ikey][jkey] = self.W[ikey][jkey] / self.W_max[jkey]

    def Recommend(self, user, K=3, N=10):
        rank = dict()  # 推荐字典
        action_item = self.train[user]  # 获取用户user的物品和评分数据

        for item, score in action_item.items():  # item为用户购买的物品，score为评分
            for j, Wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0:K]:  # self.W[item].items(
                # )为物品item的相似度矩阵
                if j in action_item.keys():  # 用户已经购买过的物品，不再推荐
                    continue
                rank.setdefault(j, 0)
                rank[j] += (Wj * score)  # j为根据相似度推荐的物品，Wj为推荐的物品和用户的物品item的相似度，score为item的评分
        return sorted(rank.items(), key=lambda x: [1], reverse=True)[0:N]


# def readFile(filename):
#     contents = []
#     f = open(filename, "rb")
#     contents = f.readlines()
#     f.close()
#     return contents
#
#
# def getRatingInfo(ratings):
#     rates = []
#     for line in ratings:
#         rate = line.split("\t".encode(encoding="utf-8"))
#         rate_str = str(int(rate[0])) + ',' + str(int(rate[2])) + ',' + str(int(rate[1]))
#         rates.append(rate_str)
#     return rates
#
#
# # 获取电影的列表
# def getMovieList(filename):
#     contents = readFile(filename)
#     movies_info = {}  # dict
#     for movie in contents:
#         single_info = movie.split("|".encode(encoding="utf-8"))  # 把当前行按|分隔，保存成list
#         movies_info[int(single_info[0])] = single_info[1:]  # 将第0个元素作为key，第二个到最后作为value保存成字典dict返回
#     return movies_info


# 获取所有电影的列表
# if __name__ == '__main__':
#
#     importlib.reload(sys)
#     movies = getMovieList("ml-100k/u.item")  # movies为dict
#     # print('movies:', movies)
#
#     contents = []
#     contents = readFile("ml-100k/u.data")
#     rates = getRatingInfo(contents)
#
#     Item = ItemBasedCF(rates)
#     # print('train:', Item.train)
#
#     Item.ItemSimilarity()
#     recommend_dict = Item.Recommend('1', 5, 20)  # k=5, N=20
#
#     print('推荐列表：')
#     recommend_list = []
#     for k, v in recommend_dict:
#         print(k + ':' + str(v))
#         recommend_list.append(int(k))
#
#     print(recommend_list)
#
#     rows = [[u"movie name", u"release", u"from userid"]]
#     for movie_id in recommend_list[:20]:
#         rows.append([movies[movie_id][0], movies[movie_id][1], " "])
