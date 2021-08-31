from importlib import import_module
from django.conf import settings

class ModuleManager: #thee who hath the modules
    def __init__(self):
        self.modules = self._get_all_modules()

    def get_module(self, module_name):
        return self.modules[module_name]
    
    def get_modules(self, module_names):
        modules = []
        for name in module_names:
            modules.append(self.modules[name])
        return modules


    def _get_all_modules(self):
        installed_apps = [app for app in settings.INSTALLED_APPS if not "django." in app]
        modules = {}
        for app in installed_apps:
            path = app.split('.')
            mod = import_module('.'.join(path[:-1]))
            conf = getattr(mod, path[-1])
            try:
                for module in conf.modules:
                    modules[module.name] = module
            except AttributeError:
                pass

        return modules
        
        

class Module:
    def __init__(self, name, img_path, title, home_view):
        self.name = name
        self.img_path = img_path
        self.title = title
        self.home_view = home_view
    """
    def __init__(self, app_name, module_name=None):
        get_modules()

        self.app_name = app_name
        module = import_module(app_name)
        self.img_path = module.apps.img_path()
        self.title = module.apps.title
        self.home_view = module.apps.home_view
    """
