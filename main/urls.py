from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path('campaign/new/<int:client_id>/', views.new_campaign, name="new_campaign"),
    path('campaign/<int:campaign_id>/', views.edit_campaign, name="edit_campaign")
]