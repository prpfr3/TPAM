from django.db import models

class BRMPlans(models.Model):

    archivenumber = models.CharField(max_length=5, default=None, blank=True, null=True)
    location = models.CharField(max_length=100, default=None, blank=True, null=True)
    description = models.CharField(max_length=2000, default=None, blank=True, null=True)
    scale = models.CharField(max_length=100, default=None, blank=True, null=True)
    number = models.CharField(max_length=100, default=None, blank=True, null=True)
    origin = models.CharField(max_length=100, default=None, blank=True, null=True)
    date = models.CharField(max_length=100, default=None, blank=True, null=True)
    tube = models.CharField(max_length=100, default=None, blank=True, null=True)
    roll = models.CharField(max_length=100, default=None, blank=True, null=True)
    drawingno = models.CharField(max_length=100, default=None, blank=True, null=True)
    negativeno = models.CharField(max_length=100, default=None, blank=True, null=True)
    material = models.CharField(max_length=100, default=None, blank=True, null=True)
    images = models.CharField(max_length=100, default=None, blank=True, null=True)
    image = models.ImageField(upload_to="images/", default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Bluebell Railway Archive Maps & Plans"
        db_table = 'notes_brmplans'

    def __str__(self):
        return f"{self.location} {self.description}"


class BRMPhotos(models.Model):

    reference_number = models.IntegerField()
    key = models.CharField(max_length=100, default=None, blank=True, null=True)
    company = models.CharField(max_length=50, default=None, blank=True, null=True)
    lococlass = models.CharField(max_length=100, default=None, blank=True, null=True)
    number = models.CharField(max_length=100, default=None, blank=True, null=True)
    date = models.CharField(max_length=100, default=None, blank=True, null=True)
    date = models.CharField(max_length=100, default=None, blank=True, null=True)
    number = models.CharField(max_length=100, default=None, blank=True, null=True)
    name = models.CharField(max_length=100, default=None, blank=True, null=True)
    location = models.CharField(max_length=100, default=None, blank=True, null=True)
    train_working = models.CharField(
        max_length=1000, default=None, blank=True, null=True
    )
    other_information = models.CharField(
        max_length=1000, default=None, blank=True, null=True
    )
    photographer = models.CharField(max_length=100, default=None, blank=True, null=True)
    photographer_ref = models.CharField(
        max_length=100, default=None, blank=True, null=True
    )
    sort_date = models.CharField(max_length=100, default=None, blank=True, null=True)
    day_of_week = models.CharField(max_length=100, default=None, blank=True, null=True)
    holiday = models.CharField(max_length=100, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Bluebell Railway Photo Archive"
        db_table = 'notes_brmphotos'

    def __str__(self):
        return f"{self.reference_number} {self.lococlass} @ {self.location}"# Create your models here.
