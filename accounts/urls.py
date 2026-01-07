
from django.urls import path,include
from . import views

urlpatterns = [
    path('client_login/',views.client_login,name='client_login' ),
    path('client_register/',views.client_register,name='client_register' ),
    path('profile/', views.client_profile_view, name='client_profile'),
    path('edit_profile/update/', views.save_client_profile, name='save_client_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('collector_register/',views.collector_register,name='collector_register' ),
    path('collector_login/',views.collector_login,name='collector_login' ),
    path('vendor_register/',views.vendor_register,name='vendor_register' ),
    path('vendor_login/',views.vendor_login,name='vendor_login' ),



]
