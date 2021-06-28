from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.overview),
    path('<int:client_pk>/', views.details),
    path('milestones/', views.list_milestones),
    path('milestones/<int:milestone_pk>/', views.edit_milestone)
]
