# -*- coding:utf-8 -*-
# @FileName  :views.PY
# @Time      :11/27/2023 1:27 PM
# @Author    :Leisang.Gam
# @contact: Leisang.Gam@outlook.com


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.models import User

from app_user.forms import RegisterForm
from app_user.models import EmailVerifyRecord, EmailInfo
from app_user.utils.send_email import send_user_email, is_smtp_server_available


class SetNewWebEmail(View):
    @staticmethod
    def post(request):
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        smtp_server = request.POST.get('email_server')
        smtp_port = request.POST.get('email_port')
        ttls = request.POST.get('ttls')
        if is_smtp_server_available(smtp_server, smtp_port, email, password, ttls):
            EmailInfo.objects.create(email=email, email_host=smtp_server, email_port=smtp_port,email_type='send')
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('邮箱配置错误')


class Home(View):
    """
    主页视图
    """

    @staticmethod
    def get(request):
        """
        GET请求处理方法
        """
        config_email = EmailInfo.objects.filter(email_type='send').exists()
        if not config_email:
            return render(request, 'new-web-setting.html', {'msg': '未配置发送邮箱'})
        return render(request, 'home.html')


class Welcome(View):
    """
    主页视图
    """

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        """
        GET请求处理方法
        """
        if request.user.is_authenticated:
            return render(request, 'welcome.html')
        else:
            return render(request, 'login.html')


class LoginView(View):
    """
    登录视图
    """

    @staticmethod
    def get(request):
        """
        根据请求获取登录页面的逻辑

        参数:
            request (HttpRequest): HTTP请求对象

        返回:
            HttpResponse: 登录页面的响应对象
        """

        before_step = request.GET.get('before_step', '/')
        if before_step:
            return render(request, 'login.html', {'before_step': before_step, 'msg': ''})
        else:
            return render(request, 'login.html', {'next_web': '', 'msg': ''})

    @staticmethod
    def post(request):
        """
        登录逻辑
        """
        before_step = request.GET.get('before_step', '')
        data = dict()
        email_or_username = request.POST.get('email_or_username', None)  # 从请求的表单数据中获取username的值
        pass_word = request.POST.get('password', None)  # 从请求的表单数据中获取password的值
        # 查询用户名为user_name的用户
        temp_user = User.objects.filter(
            Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)).first()
        user = authenticate(username=temp_user, password=pass_word)  # 对用户进行身份验证
        if not user:  # 判断用户身份验证是否成功
            msg_dict = {'msg_type': 'warning', 'content': '用户名或密码错误'}
            data['msg'] = msg_dict
            return render(request, 'login.html', data)
        login(request, user)  # 登录成功
        if before_step:  # 判断是否有下一个网址
            return HttpResponseRedirect(before_step)  # 重定向到next_web指定的网址
        return HttpResponseRedirect('/')


class RegisterView(View):
    """
    注册视图
    """

    @staticmethod
    def get(request):
        """
        获取注册页面的逻辑
        """
        before_step = request.GET.get('before_step', '')
        register_form = RegisterForm()

        return render(request, 'register.html', {
            'register_form': register_form,
            'before_step': before_step}
                      )

    @staticmethod
    def post(request):
        """
        注册逻辑

        :param request: 请求对象
        :return: 渲染的响应对象
        """
        before_step = request.GET.get('before_step', '')
        username = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        pass_word_2 = request.POST.get('password_2', '')
        # first_name = request.POST.get('first_name', None)
        # last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', '')
        request_data = request.POST
        data = dict()
        data['request_data'] = request_data
        data['before_step'] = before_step
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if User.objects.filter(username__iexact=username).exists():
                msg_dict = {'msg_type': 'warning', 'content': '用户名已经被注册，请更换一个'}
                data['msg'] = msg_dict
                return render(request, 'register.html', data)
            if User.objects.filter(email__iexact=email).exists():
                msg_dict = {'msg_type': 'warning', 'content': '邮箱已经被注册，请更换一个'}
                data['msg'] = msg_dict
                return render(request, 'register.html', data)
            if pass_word != pass_word_2:
                msg_dict = {'msg_type': 'warning', 'content': '请输入相同的密码'}
                data['msg'] = msg_dict
                return render(request, 'register.html', data)
            new_user = User()
            new_user.username = username
            # new_user.first_name = first_name
            # new_user.last_name = last_name
            new_user.email = email
            new_user.is_staff = False
            new_user.is_active = False
            new_user.password = make_password(pass_word)

            if send_user_email(email, 'register'):
                msg_dict = {'msg_type': 'success', 'content': '注册成功，请前往邮箱查看激活链接'}
                data['email_or_username'] = new_user.username
                data['msg'] = msg_dict
                new_user.save()
                return render(request, 'login.html', data)
            else:
                msg_dict = {'msg_type': 'warning', 'content': '无法发送邮件注册失败，请联系管理员'}
                data['msg'] = msg_dict
                return render(request, 'register.html', data)
        else:
            data['register_form'] = register_form
            return render(request, 'register.html', data)


class ActiveUser(View):
    """
    激活视图
    """

    @staticmethod
    def get(request, active_code):
        # 查询邮箱验证记录是否存在
        record_info = EmailVerifyRecord.objects.filter(code=active_code, send_type='register', is_active=True)
        msg_dict = {'msg_type': 'warning', 'content': '链接已失效，请点击找回密码重新激活'}
        if record_info.exists():
            for record in record_info:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                record.is_active = False
                record.save()
                break
            msg_dict = {'msg_type': 'success', 'content': '激活成功，请登录'}
        data = dict()
        data['msg'] = msg_dict
        return render(request, "login.html", data)


class FindPassword(View):
    """
    退出登录视图
    """

    @staticmethod
    def get(request):
        """
        GET请求处理方法
        """
        before_step = request.GET.get('before_step', '')
        return render(request, "find-password.html", {'before_step': before_step})

    @staticmethod
    def post(request):
        before_step = request.GET.get('before_step', '')
        input_email = request.POST.get('input_email', '')
        users = User.objects.filter(email=input_email)
        data = dict()
        data['before_step'] = before_step
        data['input_email'] = input_email
        if not users.exists():
            msg_dict = {'msg_type': 'warning', 'content': '邮箱不存在，请重新输入'}
            data['msg'] = msg_dict
            return render(request, "find-password.html", data)
        user = users.first()
        if not user.is_active:
            msg_dict = {'msg_type': 'warning', 'content': '邮箱未激活，请查看邮箱激活信息'}
            data['msg'] = msg_dict
            EmailVerifyRecord.objects.create(email=input_email, send_type='register').update(is_active=False)
            if send_user_email(input_email, 'register'):
                return render(request, "find-password.html", data)
            else:
                msg_dict = {'msg_type': 'warning', 'content': '无法发送邮件注册失败，请联系管理员'}
                data['msg'] = msg_dict
                return render(request, 'find-password.html', data)
        else:
            EmailVerifyRecord.objects.filter(email=input_email, send_type='find_password').update(is_active=False)
            if send_user_email(input_email, 'find_password'):
                msg_dict = {'msg_type': 'success', 'content': '重置密码邮件发送成功，请前往邮箱查看'}
                data['msg'] = msg_dict
                return render(request, "find-password.html", data)
            else:
                msg_dict = {'msg_type': 'warning', 'content': '无法发送邮件，请联系管理员'}
                data['msg'] = msg_dict
                return render(request, 'find-password.html', data)


class LogoutView(View):
    """
    退出登录视图
    """

    @staticmethod
    def get(request):
        """
        GET请求处理方法
        """
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect('/')


class ResetPassword(View):
    @staticmethod
    def get(request, reset_code):
        data = dict()
        all_records = EmailVerifyRecord.objects.filter(code=reset_code, send_type='find_password', is_active=True)
        data['reset_code'] = reset_code
        if all_records.exists():
            record = all_records.first()
            email = record.email
            data['email'] = email
            return render(request, "password-reset.html", data)
        else:
            msg_dict = {'msg_type': 'warning', 'content': '链接已失效，请点击找回密码重新尝试'}
            data['msg'] = msg_dict
            return render(request, "password-reset.html", data)

    @staticmethod
    def post(request, reset_code):
        pass_word = request.POST.get('password', '')
        pass_word_2 = request.POST.get('password_2', '')
        data = dict()
        data['reset_code'] = reset_code
        all_records = EmailVerifyRecord.objects.filter(code=reset_code, send_type='find_password', is_active=True)
        if not all_records.exists():
            msg_dict = {'msg_type': 'warning', 'content': '链接已失效，请点击找回密码重新尝试'}
            data['msg'] = msg_dict
            return render(request, "password-reset.html", data)
        email = all_records.first().email
        if pass_word != pass_word_2:
            msg_dict = {'msg_type': 'warning', 'content': '两次密码输入不一致，请重新输入'}
            data['msg'] = msg_dict
            return render(request, "password-reset.html", data)
        if len(pass_word) < 6:
            msg_dict = {'msg_type': 'warning', 'content': '密码长度不能小于6位'}
            data['msg'] = msg_dict
            return render(request, "password-reset.html", data)
        else:
            User.objects.filter(email=email).update(password=make_password(pass_word))
            EmailVerifyRecord.objects.filter(email=email, send_type='find_password').update(is_active=False)
            msg_dict = {'msg_type': 'success', 'content': '密码重置成功，请重新登录'}
            data['msg'] = msg_dict
            return render(request, "login.html", data)
