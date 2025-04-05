from django.apps import AppConfig


class EmrecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emrecord'
    # 通过verbose_name可以将app名改为中文
    verbose_name = '管网检测信息'
