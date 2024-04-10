from django.db import models
from notes.models import Post


class CompanyCategory(models.Model):
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category

    class Meta:
        managed = True


class Company(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.SlugField(
        max_length=250, allow_unicode=True, default=None, blank=True, null=True
    )
    code = models.CharField(max_length=10, blank=True, null=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    company_category_fk = models.ManyToManyField(CompanyCategory, blank=True)
    successor_company = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    date_formed = models.CharField(max_length=200, blank=True, null=True)
    date_succeeded = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse

        return reverse("companies:company", kwargs={"company_id": self.pk})

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name_plural = "Companies"


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.CharField(max_length=250, default=None, blank=True, null=True)
    railuk_code = models.CharField(max_length=3, blank=True, null=True)
    brd_code = models.CharField(max_length=3, blank=True, null=True)
    brsl_code = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    pre_grouping_owner = models.CharField(
        max_length=10, blank=True, default=""
    )  # pre1923
    grouping_owner = models.CharField(max_length=4, blank=True, default="")  # 1923-1947
    br_region_owner = models.CharField(
        max_length=3, blank=True, default=""
    )  # 1948-1997
    date_opened = models.CharField(max_length=10, blank=True, null=True)
    date_closed = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=77, blank=True, null=True)
    steam = models.CharField(max_length=10, blank=True, null=True)
    diesel = models.CharField(max_length=10, blank=True, null=True)
    electric = models.CharField(max_length=10, blank=True, null=True)
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse

        return reverse("companies:manufacturer", kwargs={"manufacturer_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Manufacturers"
