from django import template
from post.models import Post
register = template.Library()

@register.filter(name="liked_by")
def liked_by(post, user):
    return post.liked_by(user)

