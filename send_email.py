#! /usr/bin/python
# -*-coding:UTF-8-*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
sender = 'dxz00ww@163.com'
pwd = 'Dong-0001' #开通邮箱服务后，设置的客户端授权密码
receivers = ['836734166@qq.com'] # 接收邮件，可设置为你的邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('学分统计', 'plain', 'utf-8')
message['From'] = 'dxz00ww@163.com'
message['To'] = '836734166@qq.com'

subject = 'Dear: 大家好， 请将统计的学分发给我，谢谢'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 使用非本地服务器，需要建立ssl连接
    smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtpObj.login(sender, pwd)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException as e:
    print ("Error: 无法发送邮件.Case:%s" % e)