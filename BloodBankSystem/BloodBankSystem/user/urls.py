from django.urls import path
from user import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('donors/search/', views.search_donor, name='search_donor'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('my-requests/', views.my_blood_requests, name='my_blood_requests'),
    path('my-requests/<int:pk>/', views.blood_request_detail, name='blood_request_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
