# -*- coding:utf-8 -*-
# @FileName  :migrate_script.py.PY
# @Time      :12/5/2023 1:05 PM
# @Author    :Leisang.Gam
# @contact: Leisang.Gam@outlook.com


import os
from django.core.management import execute_from_command_line

# 设置Django的配置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_learn.settings")

# 执行数据库迁移
execute_from_command_line(["manage.py", "makemigrations", "app_user"])
# execute_from_command_line(["manage.py", "makemigrations", "app_middle_ware"])
execute_from_command_line(["manage.py", "migrate"])
