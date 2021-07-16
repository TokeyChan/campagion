from django.urls import path
from django.shortcuts import reverse

from . import views

app_name="users"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('', views.overview, name="overview")
]

def start_url():
    return reverse('users:overview')