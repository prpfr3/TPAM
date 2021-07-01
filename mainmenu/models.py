from django.db import models
from django.contrib.auth.models import User

class MyDjangoApp(models.Model):
    image = models.ImageField(upload_to='media/')
    summary = models.TextField()
    url = models.SlugField()

    def __str__(self):
        return self.summary
