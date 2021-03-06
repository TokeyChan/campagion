from django.urls import path
from django.shortcuts import reverse

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.overview, name="overview"),
    path('<int:campaign_id>/', views.workflow, name="workflow"),
    path('milestones/', views.list_milestones, name="list_milestones"),
    path('milestones/new/', views.new_milestone, name="new_milestone"),
    path('milestones/<int:milestone_id>/', views.edit_milestone, name="edit_milestone"),
    path('<int:campaign_id>/design/', views.design_workflow, name="design_workflow"),
    path('templates/<int:template_id>/<int:campaign_id>/', views.edit_template, name="edit_template"),
    path('templates/choose/<int:campaign_id>/', views.choose_template, name="choose_template"),
    path('templates/new/<int:campaign_id>/', views.new_template, name="new_template"),
    path('uploads/new/<int:task_id>/', views.upload_file, name="upload_file"),

    #background-requests
    path('js/new_milestone/<int:campaign_id>', views.bg_new_milestone, name="bg_new_milestone")
]

def start_url():
    return reverse('tracker:overview')