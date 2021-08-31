from django.apps import AppConfig
from main.contrib.utils import Module

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    modules = [
        Module(
            name = "clients",
            title = "Kundenzone",
            img_path = "/main/images/clients.png",
            home_view = "main:clients"
        )
    ]