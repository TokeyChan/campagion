from importlib import import_module
from main.models import Assignee

class Module:
    def __init__(self, app_name):
        self.app_name = app_name
        module = import_module(app_name)
        self.img_path = module.apps.img_path()
        self.title = module.apps.title
        self.home_view = module.apps.home_view
