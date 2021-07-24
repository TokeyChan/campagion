
def active_module(request):
    return {
        'ACTIVE_MODULE': request.session.get('active_module', None)
    }