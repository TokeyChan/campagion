from django.apps import AppConfig
from campagion.contrib.utils import Module

class AdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'administration'

    modules = [
        Module(
            name = "commissions",
            title = "Provisionen", 
            img_path = "administration/images/commissions.png",
            home_view = "administration:commissions",
            only_admin=False
        )
    ]
