
from django.urls import path,include
from . import views

urlpatterns = [
    path('vendor_dashboard/',views.vendor_dashboard,name='vendor_dashboard'),
    path('ewaste_req/',views.ewaste_req,name='ewaste_req'),
    path("mark-delivered/<int:assignment_id>/", views.mark_delivered, name="mark_delivered"),
    path('delivered_ewaste/',views.delivered_ewaste,name='delivered_ewaste'),
    path("generate-report/<int:assignment_id>/", views.generate_report, name="generate_report"),
    path("reports/approved/", views.approved_reports, name="approved_reports"),
    path("reports/rejected/", views.rejected_reports, name="rejected_reports"),
]
