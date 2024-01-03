from django.db import models

# Create your models here.


from django.db import models


class SystemRuntime(models.Model):
    total_runtime = models.FloatField(default=0, verbose_name='总运行时间(秒)')
    hold_runtime = models.FloatField(default=180, verbose_name='可运行时间(天)')

    class Meta:
        app_label = 'app_user'
        db_table = 'app_user_runtime'
        verbose_name = '运行时间'
        verbose_name_plural = verbose_name


class EmailInfo(models.Model):
    email_type_choices = (
        ('send', '发送邮件'),
        ('cc', '抄送的邮件'),
    )
    email = models.CharField(verbose_name='邮件名', max_length=800)
    user_name = models.CharField(verbose_name='邮箱用户名', max_length=800, blank=True, null=True, )
    password = models.CharField(verbose_name='邮箱密码', max_length=800, blank=True, null=True, )
    email_host = models.CharField(verbose_name='SMTP服务器主机', max_length=800, blank=True, null=True, )
    email_ttls = models.BooleanField(verbose_name='ttls', blank=True, null=True, )
    email_port = models.IntegerField(verbose_name='端口', blank=True, null=True, )
    email_type = models.CharField(verbose_name='邮件类型', choices=email_type_choices, max_length=80, blank=True,
                                  null=True, )

    class Meta:
        app_label = 'app_user'
        db_table = 'app_user_email_info'
        verbose_name = '发邮件信息信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=30, verbose_name='验证码类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        app_label = 'app_user'
        db_table = 'app_user_email_varify_record'
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
