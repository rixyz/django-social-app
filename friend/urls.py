from django.urls import path
from . import views

urlpatterns = [
    path('', views.FriendListView.as_view(), name='friend-list'),
    path('requests/', views.FriendAPIView.as_view(), name='request-list'),
    path('add/<int:user_id>/', views.FriendAPIView.as_view(), name='send-request'),
    path('remove/<int:friend_id>/', views.FriendAPIView.as_view(), name='unfriend'),
    path('<str:action>/<int:fr_request_id>/', views.FriendAPIView.as_view(), name='accept-request'),
    path('<str:action>/<int:fr_request_id>/', views.FriendAPIView.as_view(), name='reject-request'),
]