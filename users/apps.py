from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

def img_path():
    return "users/images/users.png"

title = "User-Management"
home_view = 'users:overview'