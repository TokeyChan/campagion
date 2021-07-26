from django.shortcuts import reverse, redirect
import re

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.regexes = ["\/users\/register\/.*\/", "\/users\/login\/", "\/admin\/login\/"]
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            for regex in self.regexes:
                if re.search(regex, request.path) is not None:
                    break;
            else:
                return redirect(reverse('users:login'))
        
        response = self.get_response(request)

        return response

