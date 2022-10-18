import string
import random, json
from app import app
from flask import Flask, request, Response, json
import smtplib  # smtplib 用于邮件的发信动作
from email.mime.text import MIMEText  # email 用于构建邮件内容
from email.header import Header  # 构建邮件头

from app.mysql_data import validate_insert


@app.route('/user/code', methods=['POST', 'GET'])
def send_email():
    email = json.dumps(request.form['email'])
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '275947878@qq.com'
    password = 'oogndmlpbwkzbjeh'
    # 收信方邮箱
    to_addr = email
    # 发信服务器
    smtp_server = 'smtp.qq.com'
    # 生成随机数
    seeds = string.digits
    random_str = random.sample(seeds, k=4)
    random_str = "".join(random_str)
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(random_str, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('Sleppy运营团队')  # 发送者
    msg['To'] = Header('尊敬的注册者')  # 接收者
    subject = '注册验证，该验证码仅在五分钟内有效'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题

    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string())
        print("邮件发送成功")
        to_addr = to_addr[1:-1]
        validate_insert(to_addr, random_str, 0)
        return Response(json.dumps({'status': 0, 'msg': "发送成功"}), content_type='application/json')

    except smtplib.SMTPException:
        print("无法发送邮件")
        return Response(json.dumps({'status': 1, 'msg': "发送失败"}), content_type='application/json')
