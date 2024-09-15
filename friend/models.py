from django.db import models
from user.models import User
from django.db.models import Q

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='reverse_friendships', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username} ({self.status})"
    

    @classmethod
    def send_friend_request(cls, from_user, to_user):
        friend, created = cls.objects.get_or_create(
            user=from_user, friend=to_user,
            defaults={'status': 'Pending'}
        )
        if not created and friend.status == 'Rejected':
            friend.status = 'Pending'
            friend.save()

        return friend

    @classmethod
    def accept_friend_request(cls, from_user, to_user):
        friend = cls.objects.filter(
            user=from_user, friend=to_user, status='Pending'
        ).first()
        if friend:
            friend.status = 'Accepted'
            friend.save()

            reverse_friendship, _ = cls.objects.get_or_create(
                user=to_user, friend=from_user,
                defaults={'status': 'Accepted'}
            )
            reverse_friendship.status = 'Accepted'
            reverse_friendship.save()

        return friend

    @classmethod
    def reject_friend_request(cls, from_user, to_user):
        friend = cls.objects.filter(
            user=from_user, friend=to_user, status='Pending'
        ).first()
        if friend:
            friend.status = 'Rejected'
            friend.save()

        return friend

    @classmethod
    def unfriend(cls, user1, user2):
        cls.objects.filter(
            (Q(user=user1, friend=user2) | Q(user=user2, friend=user1)),
            status='Accepted'
        ).delete()

    @classmethod
    def is_friend(cls, user1, user2):
        return cls.objects.filter(
            user=user1, friend=user2, status='Accepted'
        ).exists()

    @classmethod
    def get_friends(cls, user):
        return User.objects.filter(
            reverse_friendships__user=user,
            reverse_friendships__status='Accepted'
        )

    @classmethod
    def get_friend_requests(cls, user):
        return cls.objects.filter(friend=user, status='Pending')