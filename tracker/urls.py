from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.overview, name="overview"),
    path('<int:campaign_id>/', views.workflow, name="workflow"),
    path('milestones/', views.list_milestones),
    path('milestones/<int:milestone_id>/', views.edit_milestone),
    path('<int:campaign_id>/design', views.design_workflow, name="design_workflow"),

    #js calls
    path('js/update_tasks/<int:workflow_id>/', views.update_tasks),
    path('js/update_task/<int:task_id>/', views.update_task)
]
