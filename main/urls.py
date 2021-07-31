from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('campaign/new/', views.new_campaign, name="new_campaign"),
    path('campaign/<int:campaign_id>/', views.edit_campaign, name="edit_campaign"),
    path('client/new/', views.new_client, name="new_client"),
    path('client/<int:client_id>/', views.edit_client, name="edit_client"),
    path('post/', views.post_handler, name="post_handler"),
    path('js/client/new/', views.bg_new_client, name="bg_new_client")
]
