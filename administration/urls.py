from django.urls import path

from . import views

app_name = "administration"

urlpatterns = [
    path('commissions/', views.commissions_without_year, name="commissions"),
    path('commissions/<int:year>/', views.commissions, name="commissions_with_year"),
    path('commissions/js/<int:commission_id>/', views.json_commission, name="json_commission")
]