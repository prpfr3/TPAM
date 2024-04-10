from django.db import models
from django.contrib.auth.models import User

# N.B. Classes have to be listed in order such that a class refering to another appears later in the list


class NaPTANRailReferences(models.Model):
    atcocode = models.CharField(max_length=20, blank=True, null=True)
    tiploccode = models.CharField(max_length=20, blank=True, null=True)
    crscode = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelang = models.CharField(max_length=2, blank=True, null=True)
    gridtype = models.CharField(max_length=1, blank=True, null=True)
    easting = models.FloatField(blank=True, null=True)
    northing = models.FloatField(blank=True, null=True)
    creationdatetime = models.DateTimeField
    modificationdatetime = models.DateTimeField
    revisionnumber = models.SmallIntegerField(blank=True, null=True)
    modification = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = "Naptan Rail Reference"
        verbose_name_plural = "Naptan Rail References"

    def __str__(self):
        return self.name
