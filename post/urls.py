from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create_post, name='post-create'),
    path('view/<int:post_id>/', views.post_detail, name='post-detail'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('<int:post_id>/comment/add/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>', views.get_comment, name='get-comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    
]