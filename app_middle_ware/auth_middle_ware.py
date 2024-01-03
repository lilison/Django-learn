# -*- coding:utf-8 -*-
# @FileName  :auth_middle_ware.PY
# @Time      :12/18/2023 3:38 PM
# @Author    :Leisang.Gam
# @contact: Leisang.Gam@outlook.com
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# 白名单
# 将登陆、登出、验证登陆请求设为白名单，不进行用户验证。
# 这里设置了/static/静态文件，因为我这个项目静态文件没走nginx，如果静态文件通过nginx访问，可以不需要设置

excluded_path = [
    "/login/",
    "/register/",
    "/logout/",
    "/static/",
    ""
]


# 用来验证用户是否有权限登陆的中间件，在setting中间件加入'AuthUserLogin.AuthMiddleWare'
class AuthMiddleWare(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        url_path = request.path
        # 如果请求在白名单里，则通过，不进行操作
        for each in excluded_path:
            if re.match(each, url_path):
                return
        # 如果未登陆，则调转到登陆页面，将请求的url作为next参数
        if not request.user.is_authenticated:
            return redirect("/login/")
        #  如果已经登陆，则通过
        else:
            return
