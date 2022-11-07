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
        # password='password',
        password='Sleepy1234567890',
        db='sleepy',
        charset='utf8'
    )


# 查询某表的总行数、
def count_tableLine(genres, countries, syear, eyear):
    conn = mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "select movie_id from movie "
        if genres != [] or countries != [] or syear is not None or eyear is not None:
            sql = sql + "where "
            if genres is not None and genres != [] and countries is not None and countries != []:
                sql = sql + "movie_id in (select distinct movie_id from movie_genres where "
                for i in range(len(genres)):
                    sql = sql + "genre_id=%s OR " % genres[i]
                sql = sql[:-3]
                sql = sql + " UNION "
                sql = sql + "select distinct movie_id from movie_countries where "
                for i in range(len(countries)):
                    sql = sql + "country_id=%s OR " % countries[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            elif genres is not None and genres != []:
                sql = sql + "(select distinct movie_id from movie_genres where "
                for i in range(len(genres)):
                    sql = sql + "genre_id=%s OR " % genres[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            elif countries is not None and countries != []:
                sql = sql + "(select distinct movie_id from movie_countries where "
                for i in range(len(countries)):
                    sql = sql + "country_id=%s OR " % countries[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            if syear is not None:
                sql = sql + "movie.year>=%d " % syear
                sql = sql + "AND "
            if eyear is not None:
                sql = sql + "movie.year <=%d " % eyear
                sql = sql + "AND "
            sql = sql[:-4]

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


# user
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
    sql = "select * from movie where movie_id=%s" % movie_id
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


# 获取所属体裁的信息
def get_Genre(movie_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie_genres where movie_id=%s" % movie_id
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


# 获取所属国家/地区信息
def get_Country(movie_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie_countries where movie_id=%s" % movie_id
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


def update_Movielike(movie_id, uid, like_choice):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "update movie_like set like_choice=%s where uid=%s and movie_id=%s" % (like_choice, uid, movie_id)
    try:
        cursor.execute(sql)
        conn.commit()
        return 1
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 登录用户设置对电影的喜欢/不喜欢
def set_Movielike(movie_id, uid):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "insert into movie_like(uid,movie_id,like_choice) values(%s,%s,0)" % (uid, movie_id)
    try:
        cursor.execute(sql)
        conn.commit()
        return 1
    except Exception as e:
        print(e)
        print('失败')
    cursor.close()
    conn.close()
    return 0


# 登录用户判断是否喜欢该电影
def judge_Movielike(movie_id, uid):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie_like where movie_id=%s and uid=%s" % (movie_id, uid)
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


# 返回约束条件下的电影列
def search_movieList(genres, countries, syear, eyear, sortby, page, size):
    conn = mysql_conn()
    cursor = conn.cursor()
    try:
        sql = "select * from movie "
        if genres != [] or countries != [] or syear is not None or eyear is not None:
            sql = sql + "where "
            if genres is not None and genres != [] and countries is not None and countries != []:
                sql = sql + "movie_id in (select distinct movie_id from movie_genres where "
                for i in range(len(genres)):
                    sql = sql + "genre_id=%s OR " % genres[i]
                sql = sql[:-3]
                sql = sql + " UNION "
                sql = sql + "select distinct movie_id from movie_countries where "
                for i in range(len(countries)):
                    sql = sql + "country_id=%s OR " % countries[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            elif genres is not None and genres != []:
                sql = sql + "(select distinct movie_id from movie_genres where "
                for i in range(len(genres)):
                    sql = sql + "genre_id=%s OR " % genres[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            elif countries is not None and countries != []:
                sql = sql + "(select distinct movie_id from movie_countries where "
                for i in range(len(countries)):
                    sql = sql + "country_id=%s OR " % countries[i]
                sql = sql[:-3]
                sql = sql + ") AND "
            if syear is not None:
                sql = sql + "movie.year>=%d " % syear
                sql = sql + "AND "
            if eyear is not None:
                sql = sql + "movie.year <=%d " % eyear
                sql = sql + "AND "
            sql = sql[:-4]
        if sortby is not None:
            if 'rate' in sortby:
                sql = sql + "ORDER BY rating DESC "
            elif 'yearinc' in sortby:
                sql = sql + "ORDER BY year ASC "
            elif 'yeardec' in sortby:
                sql = sql + "ORDER BY year DESC "
        else:
            sql = sql + "ORDER BY movie_id "
        if size is not None and page is not None:
            sql = sql + "LIMIT %s , %s " % (size * (page - 1), size * page)
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


# 返回电影所属国家/地区id和名称
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


# 根据电影id查询影人列表
def search_moviePersons(movie_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select relationship.role, relationship.person_id, person.person_name, person.sex, person.birthday, " \
          "person.birthplace, person.person_summary, person.person_img from relationship,person where " \
          "relationship.movie_id='%s' and relationship.person_id=person.person_id" % movie_id
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


# person
# 查询影人列表
def search_personList():
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from person"
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


# 登录用户设置对影人的喜欢/不喜欢
def update_Personlike(person_id, uid, like_choice):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "update person_like set like_choice=%s where uid=%s and person_id=%s" % (like_choice, uid, person_id)
    try:
        cursor.execute(sql)
        conn.commit()
        return 1
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 设置对用户对影人的初始评价
def set_Personlike(uid, person_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "insert into person_like(uid,person_id,like_choice) values(%s,%s,0)" % (uid, person_id)
    try:
        cursor.execute(sql)
        conn.commit()
        return 1
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()
    return 0


# 登录用户判断是否喜欢该电影
def judge_Personlike(person_id, uid):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from person_like where person_id=%s and uid=%s" % (person_id, uid)
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


# 根据影人id查询其最新的五部电影
def search_personLatest(person_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie where movie_id in (select movie_id from relationship where person_id= %s ) ORDER BY " \
          "year DESC LIMIT 0,5" % person_id
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


# 根据影人id查询Top的五部电影
def search_personTop(person_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "select * from movie where movie_id in (select movie_id from relationship where person_id= %s ) ORDER BY " \
          "rating DESC LIMIT 0,5" % person_id
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


# 根据影人id查询Partner的五部电影
def search_personPartner(person_id):
    conn = mysql_conn()
    cursor = conn.cursor()
    sql = "SELECT person_id, COUNT(person_id)AS number FROM relationship WHERE movie_id IN (SELECT movie_id FROM " \
          "relationship WHERE person_id=%s)AND person_id!=%s GROUP BY person_id  ORDER BY number DESC LIMIT" \
          " 0,5" % (person_id, person_id)
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
