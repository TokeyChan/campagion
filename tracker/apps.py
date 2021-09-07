from django.apps import AppConfig
from campagion.contrib.utils import Module

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    modules = [
        Module(
            name = 'dashboard',
            title = 'Dashboard',
            img_path = "tracker/images/tracker.png",
            home_view = "tracker:overview"
        )
    ]