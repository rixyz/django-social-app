from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Friend
from user.models import User

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
    friendship = get_object_or_404(Friend, friend=friend)
    print("TEST")
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
                    'username': fr.user.username
                }
            } for fr in friend_requests
        ]
    }
    return JsonResponse(data)

@login_required
def friend_list(request):
    friends = Friend.get_friends(request.user)
    return render(request, 'friendships/friend_list.html', {'friends': friends})