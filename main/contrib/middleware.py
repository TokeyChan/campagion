from django.shortcuts import reverse, redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_path = reverse('main:login')
        if not request.user.is_authenticated:
            if request.path != login_path:
                return redirect(login_path)
        
        response = self.get_response(request)

        return response

