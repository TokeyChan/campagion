from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as login_user
from users.forms import LoginForm
from main.models import User
from users.models import Department, Invitation
from users.forms import DepartmentForm, InvitationForm, RegistrationForm
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            if user is not None:
                login_user(request, user)
                return redirect('main:index')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def register(request, key):
    invitation = Invitation.objects.get(key=key)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.create_user(request, invitation)
            return redirect('main:index')
    else:
        form = RegistrationForm(initial={'email': invitation.email})

    context = {
        'class_name': 'Registrierung',
        'form': form,
        'new': True,
        'url': reverse('users:register', kwargs={'key': key})
    }
    return render(request, 'main/simple_form.html', context)

def overview(request):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'EDIT_USER':
            user_id = int(request.POST['user_id'])
            return redirect('users:edit_user', user_id=user_id)
        if action == 'EDIT_DEPARTMENT':
            department_id = int(request.POST['department_id'])
            return redirect('users:edit_department', department_id=department_id)
        if action == 'NEW_USER':
            form = InvitationForm(request.POST)
            if form.is_valid():
                form.invite(request.user)
                messages.success(request, "Der User wurde erfolgreich eingeladen!")
                return redirect('users:overview')
            context = {
                'users': User.objects.filter(is_active=True),
                'departments': Department.objects.all(),
                'invitation_form': form,
                'edit_invitation_form': True
            }
        if action == 'NEW_DEPARTMENT':
            return redirect('users:new_department')
    else:
        context = {
            'users': User.objects.filter(is_active=True),
            'departments': Department.objects.all(),
            'invitation_form': InvitationForm()
        }
    return render(request, 'users/overview.html', context)


# Edit User und Department
def edit_user(request, user_id):
    pass

def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():
            form.save()
            return redirect('users:overview')
    else:
        form = DepartmentForm(instance=department)

    context = {
        'class_name': "Department",
        'form': form,
        'url': reverse('users:edit_department', kwargs={'department_id': department_id})
    }
    return render(request, 'main/simple_form.html', context)

def new_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:overview')
    else:
        form = DepartmentForm()

    context = {
        'class_name': "Department",
        'form': form,
        'new': True,
        'url': reverse('users:new_department')
    }
    return render(request, 'main/simple_form.html', context)