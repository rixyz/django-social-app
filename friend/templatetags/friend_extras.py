from django import template
from friend.models import Friend
register = template.Library()

@register.filter(name="is_friend")
def is_friend(user, target):
    return Friend.objects.filter(user=user, friend=target, status='Accepted').exists()

@register.filter(name="is_pending")
def is_pending(user, target):
    return Friend.objects.filter(user=user, friend=target, status='Pending').exists()

@register.filter(name="has_sent")
def has_sent(user, target):
    return Friend.objects.filter(user=target, friend=user, status='Pending').exists()
