"""
To create images in 800x600 select full size images in Windows 10 and then proceed as if sending by email to a user. 
An option will arise which allows the images to be resized.
"""

from django.core.management import BaseCommand
from notes.models import Reference
from locos.models import Image


class Command(BaseCommand):
    def handle(self, *args, **options):
        images = Reference.objects.filter(type=6)
        for image in images:
            image.delete()
            railway_image = Image()
            railway_image.image_name = image.image
            railway_image.image = image.image
            # railway_image.save()
