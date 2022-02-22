from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
    # This code signals that when a user is setup, on saving after the POST of the user, a profile should be created
    # sender = the Usermodel flags it is sending something
    # instance = the particular instance of the User
    # created = a boolean value which is True only once, when the user is created
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)