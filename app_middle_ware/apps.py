from django.apps import AppConfig


class AppMiddleWareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_middle_ware'
    verbose_name = '中间件'
