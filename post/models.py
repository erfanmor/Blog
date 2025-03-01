from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateField(default=date.today)
    view_count = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='Posts_Photo/%Y/%m/%d', default='Posts_Photo/default.png', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_likers(self):
        return {like.user.username for like in self.likes.all()}

    def likes_count(self):
        return self.likes.count()

    def get_limited_tags(self, limit=3):
        return self.tags.all()[:limit]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comments(models.Model):
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body


class CommentsReplay(models.Model):
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    replay_to = models.ForeignKey(
        'Comments', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body


class Likes(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'Like by {self.user.username} for {self.post.title}'
