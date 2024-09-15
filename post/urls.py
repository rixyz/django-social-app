from django.urls import path
from .views import PostDetailView, LikePostView, CommentView, GetCommentView, CreatePostView

urlpatterns = [
    path('new/', CreatePostView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:post_id>/comment/', CommentView.as_view(), name='add-comment'),
    path('comment/<int:comment_id>/', GetCommentView.as_view(), name='get-comment'),
    path('comment/<int:comment_id>/edit/', CommentView.as_view(), name='edit-comment'),
    path('comment/<int:comment_id>/delete/', CommentView.as_view(), name='delete-comment'),
]