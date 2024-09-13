from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.user_edit, name='edit'),  
    path('<str:username>/', views.profile, name='profile'), 
]