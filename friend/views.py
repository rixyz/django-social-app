from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Friend
from user.models import User
    
class FriendListView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'friend/friend_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return Friend.get_friends(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = [
            {
                'id': fr.id,
                'user': {
                    'id': fr.id,
                    'username': fr.username,
                    'full_name': fr.get_full_name(),
                    'profile_picture': fr.profile_picture.url,
                }
            } for fr in context['friends']
        ]
        return context

@login_required
@require_POST
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    friend = Friend.send_friend_request(request.user, to_user)
    return JsonResponse({'status': 'success', 'friend_id': friend.id})

@login_required
@require_POST
def accept_friend_request(request, fr_request_id):
    friendship = get_object_or_404(Friend, id=fr_request_id)
    if friendship.friend == request.user:  
        friendship = Friend.accept_friend_request(friendship.user, request.user)
        return JsonResponse({'status': 'success', 'friend_id': friendship.id})

@login_required
@require_POST
def reject_friend_request(request, fr_request_id):
    friendship = get_object_or_404(Friend, id=fr_request_id)
    if friendship.friend == request.user:  
        friendship = Friend.reject_friend_request(friendship.user, request.user)
        return JsonResponse({'status': 'success', 'friend_id': friendship.id})

@login_required
@require_POST
def unfriend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    friendship = get_object_or_404(Friend, friend=friend, user = request.user)
    if (friendship.user == request.user or friendship.friend == request.user):
        Friend.unfriend(request.user, friend)
        return JsonResponse({'status': 'success'})

@login_required
def friend_request_list(request):
    friend_requests = Friend.get_friend_requests(request.user)
    data = {
        'friend_requests': [
            {
                'id': fr.id,
                'user': {
                    'id': fr.user.id,
                    'username': fr.user.username,
                    'profile_picture': fr.user.profile_picture.url,
                }
            } for fr in friend_requests
        ]
    }
    return JsonResponse(data)