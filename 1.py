# import datetime, re
# import time
#
# import pymysql

# pymysql.install_as_MySQLdb()
# conn = pymysql.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='password',
#     db='sleepy',
#     charset='utf8'
# )
# cursor = conn.cursor()
# sql = "select validity_time from register_validate"
# cursor.execute(sql)
# description = cursor.description
# column_list = [column[0] for column in description]
# dt = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print(dt)
# results = cursor.fetchall()
# uid = []
# # for row in results:
# #     uid.append(row[0])
# #
# #     print("uid=%s" % uid)
# # print(str(uid[1] - uid[0]))
#
# ttime=re.split(' |-|:', dt)
# print(ttime)
# print(int(''.join(ttime)))
# cursor.close()
# conn.close()

# import string
# import random, json
# from app import app
# from flask import Flask, request, Response, json
# import smtplib  # smtplib 用于邮件的发信动作
# from email.mime.text import MIMEText  # email 用于构建邮件内容
# from email.header import Header  # 构建邮件头
#
# from app.mysql_data import validate_insert
#
#
# # @app.route('/user/code', methods=['POST', 'GET'])
# def send_email():
#     # email = request.form['email']
#     email = '2338161577@qq.com'
#     # 发信方的信息：发信邮箱，QQ 邮箱授权码
#     from_addr = '275947878@qq.com'
#     password = 'oogndmlpbwkzbjeh'
#     # 收信方邮箱
#     to_addr = email
#     # 发信服务器
#     smtp_server = 'smtp.qq.com'
#     # 生成随机数
#     seeds = string.digits
#     random_str = random.sample(seeds, k=4)
#     random_str = "".join(random_str)
#     # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
#     msg = MIMEText(random_str, 'plain', 'utf-8')
#     # 邮件头信息
#     msg['From'] = Header('Sleppy运营团队')  # 发送者
#     msg['To'] = Header('尊敬的注册者')  # 接收者
#     subject = '注册验证，该验证码仅在五分钟内有效'
#     msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
#
#     try:
#         smtpobj = smtplib.SMTP_SSL(smtp_server)
#         # 建立连接--qq邮箱服务和端口号（可百度查询）
#         smtpobj.connect(smtp_server, 465)
#         # 登录--发送者账号和口令
#         smtpobj.login(from_addr, password)
#         # 发送邮件
#         smtpobj.sendmail(from_addr, to_addr, msg.as_string())
#         print("邮件发送成功")
#         validate_insert(to_addr, random_str, 0)
#     except smtplib.SMTPException:
#         print("无法发送邮件")
# send_email()
import datetime
import pymysql
import re


# def search_code(email, code):
#     conn = pymysql.connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         password='password',
#         db='sleepy',
#         charset='utf8'
#     )
#     cursor = conn.cursor()
#     try:
#         sql = "select validity_time from register_validate where email='%s'and captcha=%s" % (email, code)
#         cursor.execute(sql)
#         if cursor is not None:  # 注意这里。单纯判断cursor是否为None是不够的
#             row = cursor.fetchone()
#             if row is not None:
#                 time_get = str(row[0])
#                 print(time_get)
#                 time_get = re.split(' |-|:', time_get)
#                 time_get = int(''.join(time_get))
#                 print(time_get)
#                 dt = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 dt = re.split(' |-|:', dt)
#                 dt = int(''.join(dt))
#                 if dt - time_get <= 500:
#                     return 1
#                 else:
#                     return 0
#             else:
#                 return 'error1'
#         else:
#             return 'error2'
#     except Exception as e:
#         print(e)
#     cursor.close()
#     conn.close()
#
#
# print(search_code('123456@qq.com', '5678'))
# if search_code('123456@qq.com', '5678') == 1:
#     print(111)
# else:
#     print(9999)

def search_user():
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='password',
        db='sleepy',
        charset='utf8'
    )
    cursor = conn.cursor()
    sql = "select country from movie "
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


uid = search_user()
a = str(uid[0])

print(a)
# for i in range(len(uid)):
#     print(uid[i])

# movie
# 查询电影基本信息
# def search_movieDetail(movie_id):
#     conn = pymysql.connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         password='password',
#         db='sleepy',
#         charset='utf8'
#     )
#     cursor = conn.cursor()
#     sql = "select * from movie where id='%s'" % movie_id
#     try:
#         cursor.execute(sql)
#         if cursor is not None:
#             results = cursor.fetchone()
#             if results is not None:
#                 cursor.close()
#                 conn.close()
#                 return results
#     except Exception as e:
#         print(e)
#         print('没有这部电影')
#     cursor.close()
#     conn.close()
#     return 0
# a=search_movieDetail('1291543')
# print(a[9])
