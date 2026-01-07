
from django.urls import path,include
from . import views

urlpatterns = [
    path('client_dashboard/',views.client_dashboard,name='client_dashboard' ),
    path('photo_list/',views.photo_list,name='photo_list' ),

    path("report/<int:photo_id>/", views.view_report, name="view_report"),
    path("report/approve/<int:report_id>/", views.approve_report, name="approve_report"),
    path("report/reject/<int:report_id>/", views.reject_report, name="reject_report"),





]
