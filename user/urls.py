from django.urls import path
from . import views

from .views import ProfileView, UserUpdateView

urlpatterns = [
    path('edit/', UserUpdateView.as_view(), name='edit'),  
    path('<str:username>/', ProfileView.as_view(), name='profile'), 
]