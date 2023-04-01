from django.db import models
from django.contrib.auth.models import User

class MyDjangoApp(models.Model):
    image = models.ImageField(upload_to='media/')
    summary = models.TextField()
    url = models.SlugField()
    order = models.IntegerField()

    def __str__(self):
        return self.summary

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"profile of the user {self.user.username}"