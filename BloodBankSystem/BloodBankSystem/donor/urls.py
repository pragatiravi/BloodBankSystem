from django.urls import path
from donor import views

urlpatterns = [
    path('register/', views.donor_register, name='donor_register'),
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('profile/', views.donor_profile, name='donor_profile'),
    path('blood-requests/', views.view_blood_requests, name='donor_blood_requests'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
]
