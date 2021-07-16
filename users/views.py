from django.shortcuts import render, redirect
from django.contrib.auth import login as login_user
from users.forms import LoginForm

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            if user is not None:
                login_user(request, user)
                return redirect('tracker:overview')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def overview(request):
    pass