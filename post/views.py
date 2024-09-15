from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .models import Post, Comment
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']
    template_name = 'post/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post-detail', post_id=post.id)
        else:
            context = self.get_context_data(object=post)
            context['comment_form'] = comment_form
            return render(request, self.template_name, context)
    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.liked_by(request.user):
            post.unlike(request.user)
            liked = False
        else:
            post.like(request.user)
            liked = True
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
class GetCommentView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return JsonResponse({
            'comment_id': comment.id,
            'content': comment.content,
            'author': comment.user.username,
            'created_at': comment.created_at,
        }) 

class CommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
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
    
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.can_edit(request.user):
            put = QueryDict(request.body)
            content = put.get('content')
            if not content:
                return JsonResponse({'success': False, 'errors': {'content': 'Content is required.'}}, status=400)
            comment.content = content
            comment.save()
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'author': comment.user.username,
                'content': comment.content,
            })
        else:
            return JsonResponse({'success': False, 'errors': {'permission': 'You do not have permission to edit this comment.'}}, status=403)
        
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.can_delete(request.user):
            comment.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': {'permission': 'You do not have permission to delete this comment.'}}, status=403) 