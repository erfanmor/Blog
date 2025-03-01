from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date


class CustomUser(AbstractUser):
    name = models.TextField(max_length=30, default='None')
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='Profile/%Y/%m/%d', default='Profile/default_user_icon.jpg')
    number = models.IntegerField(null=True, blank=True)
    date = date = models.DateField(default=date.today)
    address = models.TextField(max_length=200, default='None')

    # Social Medias
    website = models.TextField(max_length=50, default='None', blank=True)
    gitHub = models.TextField(max_length=50, default='None', blank=True)
    twitter = models.TextField(max_length=50, default='None', blank=True)
    instagram = models.TextField(max_length=50, default='None', blank=True)
    facebook = models.TextField(max_length=50, default='None', blank=True)

    def __str__(self):
        return self.username
