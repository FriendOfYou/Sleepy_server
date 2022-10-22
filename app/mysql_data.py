import datetime
import pymysql
import re

pymysql.install_as_MySQLdb()


# 连接数据库
def mysql_conn():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        # password='Sleepy1234567890',
        db='sleepy',
        charset='utf8'
    )


# user
# 检索所有，施工中，需完善
def select_all(data_list):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select *from %s" % data_list
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        uid = row[0]
        name = row[1]
        email = row[2]
        password = row[3]
        print("uid=%s,name=%s,email=%s,password=%s" % (uid, name, email, password))
    cursor.close()
    conn.close()


# 注册新用户，向register_validate中存入数据
def validate_insert(email, captcha, available):
    conn = mysql_conn()
    cursor = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt = "".join(dt)
    sql = "insert into register_validate(email,captcha,available,validity_time) values('%s',%s,%d,'%s')" % (
        email, captcha, available, dt)
    print(1)
    try:
        cursor.execute(sql)
        conn.commit()
        print("成功")
    except Exception as e:
        print(e)
        print('失败')
    cursor.close()
    conn.close()


# 注册时有效查询，验证码在register_validate表中搜索验证码的某条例子
def search_code(email, code):
    conn = mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "select validity_time from register_validate where email='%s'and captcha='%s'" % (email, code)
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            print("row=%s" % row)
            if row is not None:
                time_get = str(row[0])
                time_get = re.split(' |-|:', time_get)
                time_get = int(''.join(time_get))
                dt = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                dt = re.split(' |-|:', dt)
                dt = int(''.join(dt))
                # 有效期在五分钟内
                if dt - time_get <= 500:
                    cursor.close()
                    conn.close()
                    return 1
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 注册成功，向user表中插入新的用户信息
def insert_user(name, email, password):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "insert into user(name,email,password) values('%s','%s','%s')" % (name, email, password)
    try:
        cursor.execute(sql)
        conn.commit()
        sql = "select uid from user where name='%s' and email='%s' and password='%s'" % (name, email, password)
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            if row is not None:
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return -1


# 登录用户查询
def search_user(email, password):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select uid,name from user where email='%s' and password='%s'" % (email, password)
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            if row is not None:
                cursor.close()
                conn.close()
                print(row)
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# movie
# 根据电影id查询电影基本信息
def search_movieDetail(movie_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie where movie_id='%s'" % movie_id
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
        print('没有这部电影')
    cursor.close()
    conn.close()
    return 0


# 登录用户判断是否喜欢该电影
def judge_like(movie_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie_like where movie_id='%s'" % movie_id
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 未完成
# 返回约束条件下的电影列
def search_movieList(genres, countries, years):
    conn = mysql_conn()
    cursor = conn.cursor()
    try:
        if genres != [] and countries != [] and years != []:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif genres != [] and countries != []:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif genres != [] and years != []:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif countries != [] and years != []:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif genres:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif countries:
            sql = "select * from movie"
            # sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql)
        elif years:
            sql = "select *from movie where year in (%s)" % ','.join(['%s'] * len(years))
            cursor.execute(sql, years)
        else:
            sql = "select * from movie"
            cursor.execute(sql)

        if cursor is not None:
            row = cursor.fetchall()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 返回电影所属国家、地区id和名称
def get_movieCountries():
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from country"
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchall()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 返回genre标签
def get_movieGenres():
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from genre"
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchall()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 未完成
# 根据电影id查询影人列表
def search_moviePersons(movie_id):
    conn = mysql_conn()
    # cursor = conn.cursor()
    # sql = "select * from movie where id='%s'" % movie_id
    # try:
    #     cursor.execute(sql)
    #     if cursor is not None:
    #         row = cursor.fetchone()
    #         if row is not None:
    #             cursor.close()
    #             conn.close()
    #             return row
    # except Exception as e:
    #     print(e)
    #     print('没有这部电影')
    # cursor.close()
    # conn.close()
    # return 0


# person
# 根据影人id查询影人基本信息
def search_personDetail(person_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from person where person_id='%s'" % person_id
    try:
        cursor.execute(sql)
        if cursor is not None:
            row = cursor.fetchone()
            if row is not None:
                cursor.close()
                conn.close()
                return row
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0
