import cntext as ct


class TextAnalysis:
    def __init__(self, text, lang='chinese'):
        self.text = text
        self.lang = lang

    # 可读性
    def readability(self):
        return ct.readability(text=self.text, lang=self.lang).get("readability3")

    # 情感强度
    def sentiment_by_valence(self):
        dictionary = ct.load_pkl_dict('ChineseEmoBank.pkl')['ChineseEmoBank']
        return ct.sentiment_by_valence(text=self.text, lang=self.lang, diction=dictionary)

    # 情感
    def sentiment(self):
        dictionary = ct.load_pkl_dict('DUTIR.pkl')['DUTIR']
        return ct.sentiment(text=self.text, lang=self.lang, diction=dictionary)

    # 积极性
    def positivity(self):
        dictionary = ct.load_pkl_dict('Chinese_Loughran_McDonald_Financial_Sentiment.pkl')[
            'Chinese_Loughran_McDonald_Financial_Sentiment']
        return ct.sentiment(text=self.text, lang=self.lang, diction=dictionary)

    # 词频
    def frequency(self):
        return ct.term_freq(text=self.text, lang=self.lang)

    # 可读性
    async def readability_async(self):
        return ct.readability(text=self.text, lang=self.lang).get("readability3")

    # 情感强度
    async def sentiment_by_valence_async(self):
        dictionary = ct.load_pkl_dict('ChineseEmoBank.pkl')['ChineseEmoBank']
        return ct.sentiment_by_valence(text=self.text, lang=self.lang, diction=dictionary)

    # 情感
    async def sentiment_async(self):
        dictionary = ct.load_pkl_dict('DUTIR.pkl')['DUTIR']
        return ct.sentiment(text=self.text, lang=self.lang, diction=dictionary)

    # 积极性
    async def positivity_async(self):
        dictionary = ct.load_pkl_dict('Chinese_Loughran_McDonald_Financial_Sentiment.pkl')[
            'Chinese_Loughran_McDonald_Financial_Sentiment']
        return ct.sentiment(text=self.text, lang=self.lang, diction=dictionary)

    # 词频
    async def frequency_async(self):
        return ct.term_freq(text=self.text, lang=self.lang)

# if __name__ == '__main__':
    # comment_data = selectComment(1291543)
    # if comment_data != 0 and len(comment_data) != 0:
    #     good = []
    #     bad = []
    #     for i in range(len(comment_data)):
    #         text = comment_data[i][1]
    #         s = TextAnalysis(text=text)
    #         good_bad = s.positivity()
    #         if good_bad['negative_num'] < good_bad['positive_num']:
    #             good.append(
    #                 {'comment': comment_data[i][1], 'readability': s.readability(),
    #                  'valence': s.sentiment_by_valence()['valence']})
    #         elif good_bad['negative_num'] > good_bad['positive_num']:
    #             bad.append(
    #                 {'comment': comment_data[i][1], 'readability': s.readability(),
    #                  'valence': s.sentiment_by_valence()['valence']})
    #     good.sort(key=lambda x: x['readability'])
    #     bad.sort(key=lambda x: x['readability'])
    #     good = good[:3]
    #     bad = bad[:3]
    #     positive = []
    #     negative = []
    #     for i in range(len(good)):
    #         positive.append(
    #             {'movie_id': comment_data[0][2], 'text': good[i]['comment'], 'readability': good[i]['readability'],
    #              'valence': good[i]['valence']})
    #         negative.append(
    #             {'movie_id': comment_data[0][2], 'text': bad[i]['comment'], 'readability': bad[i]['readability'],
    #              'valence': bad[i]['valence']})
    # #     return Response(json.dumps({'status': 0,
    # #                                 'data': {'positive': positive, 'negative': negative},
    # #                                 'msg': "评论返回成功"}), content_type='application/json')
    # # elif len(comment_data)==0:
    # #     return Response(json.dumps({'status': 0,
    # #                                 'data': None,
    # #                                 'msg': "评论条数空"}), content_type='application/json')
    # # else:
    # #     return Response(json.dumps({'status': 1, 'data': None, 'msg': "评论返回失败"}),
    # #                 content_type='application/json')
    # text = "这部电影很难看，很无聊，不推荐。"
    # text2 = "看哭了的喜剧"
    # s = TextAnalysis(text=text2)
    # print(s.readability())
    # print(s.positivity())
    # print(s.sentiment_by_valence())
