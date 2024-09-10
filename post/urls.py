from django.urls import path
from . import views
urlpatterns = [
    path('new/', views.create_post, name='post-create'),
]