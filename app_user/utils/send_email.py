# -*- coding:utf-8 -*-
# @FileName  :send_email.PY
# @Time      :12/22/2023 9:45 PM
# @Author    :Leisang.Gam
# @contact: Leisang.Gam@outlook.com
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from django_middleware_global_request.middleware import get_request

from app_user.models import EmailVerifyRecord, EmailInfo


def self_send_email(
        email_title: str,
        receive_body: str,
        receive_email: list[str],
        cc_list: Optional[list[str]] = None) -> str:
    """
    使用配置的SMTP服务器发送邮件。

    参数:
    - email_title (str): 邮件的标题。
    - receive_body (str): 邮件的内容/正文。
    - receive_email (List[str]): 接收邮件的邮箱地址列表。
    - cc_list (Optional[List[str]]): 抄送（CC）的邮箱地址列表，默认为空列表。

    返回:
    - str: 包含邮件发送过程状态的消息。
    """

    # 如果未提供 cc_list，则将其设置为空列表
    if cc_list is None:
        cc_list = []

    # 从数据库中获取邮件配置信息
    send_email = EmailInfo.objects.filter(email_type='send')

    if send_email.exists():
        send_email_info = send_email.first()

        # 从数据库中提取SMTP服务器详细信息
        smtp_server = send_email_info.email_host  # SMTP服务器主机
        smtp_port = send_email_info.email_port  # 端口
        sender_email = send_email_info.email  # 发件人邮箱地址
        password = send_email_info.password  # 密码
        ttls = send_email_info.email_ttls  # 是否使用TLS加密

        # 创建邮件内容
        subject = email_title
        body = receive_body
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ",".join(receive_email)

        # 如果提供了 CC，添加到邮件中
        if cc_list:
            message["Cc"] = ",".join(cc_list)

        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # 发送邮件
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if ttls:
                    server.starttls()  # 使用TLS加密通信
                server.login(sender_email, password)
                server.sendmail(sender_email, receive_email + cc_list, message.as_string())
            tips = "邮件发送成功！"
        except Exception as e:
            tips = "发送邮件时出现错误：" + str(e)
    else:
        tips = '请先配置发送邮件信息'

    return tips


def send_user_email(email, send_type="register"):
    request = get_request()
    homepage = request.META['HTTP_HOST']
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code = str(uuid.uuid4()).split('-')[-1]
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    # 定义邮件内容:
    email_title = ""
    email_body = ""
    if send_type == "register":
        email_title = "欢迎注册本站，激活链接"
        email_body = "请点击下面的链接激活你的账号: " + homepage + "/active/{0}".format(
            code)

    if send_type == "find_password":
        email_title = "点击链接找回密码"
        email_body = "请点击下面的链接找回你的密码: " + homepage + "/password-reset/{0}".format(
            code)

    try:
        self_send_email(email_title, email_body, [email])
        email_record.save()
        return True
    # 如果发送成功
    except Exception as e:
        print(str(e))
        return False


def is_smtp_server_available(smtp_server, smtp_port, sender_email, password, ttls):
    """
    检查SMTP服务器是否可用。

    Parameters:
    - smtp_server (str): SMTP服务器主机。
    - smtp_port (int): 端口。
    - sender_email (str): 发件人邮箱地址。
    - password (str): 密码。
    - ttls (bool): 是否使用TLS加密。

    Returns:
    - int or str: 如果SMTP服务器可用，返回1；否则返回包含错误信息的字符串。
    """
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if ttls:
                server.starttls()  # 使用TLS加密通信
            server.login(sender_email, password)
            tips = "配置成功！"
            return True, tips
    except Exception as e:
        tips = "SMTP服务器不可用或者密码错误：" + str(e)
        return False, tips
