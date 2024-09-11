from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/', views.user_edit, name='edit'),
]