from django.urls import path
from . import views

urlpatterns = [
    path('', views.friend_list, name='friend_list'),
    path('add/<int:user_id>/', views.send_friend_request, name='send-request'),
    path('accept/<int:fr_request_id>/', views.accept_friend_request, name='accept-request'),
    path('reject/<int:fr_request_id>/', views.reject_friend_request, name='reject-request'),
    path('remove/<int:user_id>/', views.unfriend, name='unfriend'),
    path('requests/', views.friend_request_list, name='request-list'),
]