from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

def img_path():
    return ""

title = "Kundenzone"
home_view = "main:clients"