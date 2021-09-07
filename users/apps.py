from django.apps import AppConfig
from campagion.contrib.utils import Module

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    modules = [
        Module(
            name = "users",
            title = "User-Management",
            img_path = "users/images/users.png",
            home_view = "users:overview"
        )
    ]