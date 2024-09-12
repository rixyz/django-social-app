from django.db import models
from user.models import User

class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Post(CreatedAtModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)

    def liked_by(self, user):
        return self.likes.filter(user=user).exists()

    def like(self, user):
        Like.objects.create(post=self, user=user)

    def unlike(self, user):
        Like.objects.filter(post=self, user=user).delete()

class Comment(CreatedAtModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)

    def can_edit(self, user):
        return self.user == user

    def can_delete(self, user):
        return self.user == user or self.post.author == user

    @classmethod
    def get_post_comments(cls, post_id):
        return cls.objects.filter(post__id=post_id)

    class Meta:
        get_latest_by = 'created_at'

class Like(CreatedAtModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user',)

    @classmethod
    def get_post_likes(cls, post_id):
        return cls.objects.filter(post__id=post_id)