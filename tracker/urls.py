from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.overview, name="overview"),
    path('<int:campaign_id>/', views.workflow, name="workflow"),
    path('milestones/', views.list_milestones),
    path('milestones/<int:milestone_id>/', views.edit_milestone),
    path('<int:campaign_id>/design/', views.design_workflow, name="design_workflow"),
    path('templates/<int:template_id>/', views.edit_template, name="edit_template"),
    path('templates/choose/<int:campaign_id>', views.choose_template, name="choose_template")
]
