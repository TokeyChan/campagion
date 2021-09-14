from django.urls import path

from . import views
from . import js_views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('campaign/new/', views.new_campaign, name="new_campaign"),
    path('campaign/<int:campaign_id>/', views.edit_campaign, name="edit_campaign"),
    path('client/new/', views.new_client, name="new_client"),
    path('client/<int:client_id>/', views.edit_client, name="edit_client"),
    path('clients/', views.clients, name="clients"),
    path('post/', views.post_handler, name="post_handler"),
    path('js/client/new/', views.bg_new_client, name="bg_new_client"),
    path('js/api_data/stats/campaign/', js_views.api_stats_campaign, name="api_data"),
    path('js/api_data/stats/minicampaign/', js_views.api_stats_minicampaign, name="api_data_mini"),
    path('js/api_data/sum/campaign/', js_views.api_sum_campaign, name="api_sum"),
    path('js/api_data/sum/minicampaign/', js_views.api_sum_minicampaign, name="api_sum_mini"),
    path('js/api_data/campaign/minicampaigns/', js_views.api_minicampaigns, name="api_get_minicampaigns")
]
