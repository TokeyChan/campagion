from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.main, name="index"),
    path('users/', views.users, name="user_management"),
    path('campaign/new/<int:client_id>/', views.new_campaign, name="new_campaign"),
    path('campaign/<int:campaign_id>/', views.edit_campaign, name="edit_campaign"),
    path('client/new/', views.new_client, name="new_client"),
    path('client/<int:client_id>/', views.edit_client, name="edit_client"),
    path('post/', views.post_handler, name="post_handler")
]
