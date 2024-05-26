from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/img/default_avatar.png'


class Topic(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Explanation(models.Model):
    topic = models.ForeignKey(Topic, related_name='explanations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'

    @property
    def total_up_votes(self):
        return self.votes.filter(vote_type='up').count()

    @property
    def total_down_votes(self):
        return self.votes.filter(vote_type='down').count()

    @property
    def total_favorites(self):
        return self.favorites.count()

    @property
    def total_votes(self):
        return self.total_up_votes - self.total_down_votes


class UserVote(models.Model):
    VOTE_TYPES = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    explanation = models.ForeignKey(Explanation, related_name='votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=5, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'explanation')


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    explanation = models.ForeignKey(Explanation, related_name='favorites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'explanation')

