from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

def img_path():
    return "/main/images/clients.png"

title = "Kundenzone"
home_view = "main:clients"