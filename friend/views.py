from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Friend
from user.models import User
from .serializers import FriendSerializer
from .permissions import IsOwnerOrReadOnly

class FriendAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        """
        Retrieve a list of the user's friend requests.
        """
        friend_requests = Friend.get_friend_requests(request.user)
        serializer = FriendSerializer(friend_requests, many=True) 
        return Response(serializer.data)

    def post(self, request, user_id):
        """
        Send a friend request to another user.
        """
        to_user = get_object_or_404(User, pk=user_id)
        if request.user == to_user:
            return Response({'error': 'Cannot send a friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend = Friend.send_friend_request(request.user, to_user)
            return Response({'status': 'success', 'friend_id': friend.id}, status=status.HTTP_201_CREATED)
        except :
            return Response({'error': 'Failed to send friend request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, action, fr_request_id):
        """
        Accept or reject a friend request.
        """
        friendship = get_object_or_404(Friend, pk=fr_request_id)

        if friendship.friend != request.user:
            return Response({'error': 'You cannot accept or reject this request'}, status=status.HTTP_403_FORBIDDEN)

        if action == 'accept':
            friendship = Friend.accept_friend_request(friendship.user, request.user)
            return Response({'status': 'success', 'friend_id': friendship.id})
        elif action == 'reject':
            friendship.delete()
            return Response({'status': 'success'})
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, friend_id):
        """
        Unfriend another user.
        """

        friend = get_object_or_404(User, id=friend_id)
        friendship = get_object_or_404(Friend, friend = friend, user = request.user)

        if not (friendship.user == request.user or friendship.friend == request.user):
            return Response({'error': 'You cannot unfriend this user'}, status=status.HTTP_403_FORBIDDEN)

        Friend.unfriend(request.user, friend)
        return Response({'status': 'success'})

class FriendListView(LoginRequiredMixin, ListView):
    """
    List view for user's friend list
    """

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
            } for fr in context['friends'] # "context must be a dict rather than QuerySet"
        ]
        return context