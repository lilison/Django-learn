# -*- coding:utf-8 -*-
# @FileName  :forms.PY
# @Time      :11/27/2023 1:29 PM
# @Author    :Leisang.Gam
# @contact: Leisang.Gam@outlook.com

# users/forms.py

"""
在Django中，使用forms模块来定义表单。
LoginForm和RegisterForm是两个继承自forms.Form的类。
LoginForm类用于登录表单验证。其中，username字段不能为空，password字段不能为空且最小长度为6。
RegisterForm类用于注册验证表单。其中，username字段不能为空，password字段不能为空且最小长度为6。
"""

from django import forms


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(
        required=True,
        min_length=1,
        label="用户名",
        error_messages={
            "required": "用户名不能为空"
        }
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label="密码",
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度不能小于6位"
        }
    )


class RegisterForm(forms.Form):
    """注册验证表单"""
    # 用户名密码不能为空
    username = forms.CharField(
        required=True,
        min_length=1,
        label="用户名",
        error_messages={
            "required": "用户名不能为空"
        }
    )
    email = forms.EmailField(
        required=True,
        label="邮箱",
        error_messages={
            "required": "邮箱不能为空"
        }
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label="密码",
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度不能小于6位"
        }
    )
    password_2 = forms.CharField(
        required=True,
        min_length=6,
        label="确认密码",
        error_messages={
            "required": "确认密码不能为空",
            "min_length": "确认密码长度不能小于6位"
        }
    )
