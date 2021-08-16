from main.contrib.utils import Module

def active_module(request):
    module_name = request.session.get('active_module', None)
    if module_name:
        return {
            'ACTIVE_MODULE': Module(module_name)
        }
    return {}