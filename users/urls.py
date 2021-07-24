from django.urls import path
from django.shortcuts import reverse

from . import views

app_name="users"

urlpatterns = [
    path('', views.overview, name="overview"),
    path('login/', views.login, name="login"),
    path('edit/<int:user_id>/', views.edit_user, name="edit_user"),
    path('department/<int:department_id>/', views.edit_department, name="edit_department"),
    path('department/new/', views.new_department, name="new_department")
]