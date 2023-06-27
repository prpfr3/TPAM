from django.db import models
from .models import *
from notes.models import Post, Reference


class Role(models.Model):
    role = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.role

    class Meta:
        managed = True


class Person(models.Model):
    SOURCE_TYPE = (
        (1, "Wikipedia"),
        (2, "Custom"),
        (3, "South Western Railway Magazine"),
    )

    name = models.CharField(max_length=100, blank=True, default="")
    firstname = models.CharField(max_length=100, default=None)
    surname = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    birthdate = models.CharField(max_length=10, blank=True, default="")
    birthplace = models.CharField(max_length=200, blank=True, default="")
    dieddate = models.CharField(max_length=10, blank=True, default="")
    diedplace = models.CharField(max_length=200, blank=True, default="")
    nationality = models.CharField(max_length=200, blank=True, default="")
    occupation = models.CharField(max_length=200, blank=True, default="")
    wikitextslug = models.CharField(max_length=200, blank=True, default="")
    wikiimageslug = models.CharField(max_length=200, blank=True, default="")
    wikiimagetext = models.CharField(max_length=200, blank=True, default="")
    gracetextslug = models.CharField(max_length=200, blank=True, default="")
    roles = models.ManyToManyField(Role, through="PersonRole", blank=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    references = models.ManyToManyField(Reference, blank=True)
    source = models.IntegerField(
        choices=SOURCE_TYPE,
        default=1,
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "People"
        ordering = ("name",)


class PersonRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_from = models.CharField(max_length=10, blank=True, default="")
    date_to = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return f"{self.person.__str__} {self.role.__str__}"

    class Meta:
        verbose_name = "Person Role"
        verbose_name_plural = "People Role"
