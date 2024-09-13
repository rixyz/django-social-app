from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm

def home(request):
    context = {
        'posts': Post.objects.all(),
        'user': request.user,
    }
    return render(request, 'post/home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post/create.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'post/detail.html', context)

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.liked_by(request.user):
        post.unlike(request.user)
        liked = False
    else:
        post.like(request.user)
        liked = True
    
    response_data = {
        'liked': liked,
        'likes_count': post.likes.count()
    }
    return JsonResponse(response_data)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'content': comment.content,
            'author': comment.user.username,
            'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p')
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def get_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return JsonResponse({
        'id': comment.id,
        'content': comment.content,
        'author': comment.user.username,
        'created_at': comment.created_at,
    })

@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if not comment.can_edit(request.user):
        raise PermissionDenied
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        comment = form.save()
        return JsonResponse({
            'success': True,
            'author': comment.user.username,
            'content': comment.content,
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if not comment.can_delete(request.user):
        raise PermissionDenied
    comment.delete()
    return JsonResponse({'success': True})