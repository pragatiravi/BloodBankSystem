from django.urls import path
from bbadmin import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.admin_profile, name='admin_profile'),
    
    # Blood Group URLs
    path('blood-groups/', views.blood_group_list, name='blood_group_list'),
    path('blood-groups/add/', views.blood_group_add, name='blood_group_add'),
    path('blood-groups/<int:pk>/update/', views.blood_group_update, name='blood_group_update'),
    path('blood-groups/<int:pk>/delete/', views.blood_group_delete, name='blood_group_delete'),
    
    # Donor Management URLs
    path('donors/', views.donor_list, name='admin_donor_list'),
    path('donors/<int:pk>/', views.donor_detail, name='admin_donor_detail'),
    path('donors/<int:pk>/delete/', views.donor_delete, name='admin_donor_delete'),
    
    # Contact Query URLs
    path('contact-queries/', views.contact_query_list, name='contact_query_list'),
    path('contact-queries/<int:pk>/', views.contact_query_detail, name='contact_query_detail'),
    path('contact-queries/<int:pk>/delete/', views.contact_query_delete, name='contact_query_delete'),
    
    # Blood Request URLs
    path('blood-requests/', views.blood_request_list, name='admin_blood_request_list'),
    path('blood-requests/<int:pk>/', views.blood_request_detail, name='admin_blood_request_detail'),
    path('blood-requests/<int:pk>/delete/', views.blood_request_delete, name='admin_blood_request_delete'),
    path('blood-requests/report/', views.blood_request_report, name='blood_request_report'),
]
