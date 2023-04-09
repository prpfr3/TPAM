from django.db import models
from notes.models import Post
from locos.models import LocoClass
from people.models import Person


class CompanyCategory(models.Model):
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category

    class Meta:
        managed = True


class Company(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.SlugField(
        max_length=250, allow_unicode=True, default=None, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    company_category_fk = models.ManyToManyField(CompanyCategory, blank=True)
    lococlass_owneroperator = models.ManyToManyField(
        LocoClass, through='ClassOwnerOperator', related_name="company_owneroperator")
    lococlass_designed = models.ManyToManyField(
        LocoClass, through='ClassDesigner', related_name="company_designer")
    lococlass_built = models.ManyToManyField(
        LocoClass, through='ClassManufacturer', related_name="company_manufacturer")

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse
        return reverse('companies:company', kwargs={'company_id': self.pk})

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name_plural = 'Companies'


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.SlugField(
        max_length=250, allow_unicode=True, default=None, blank=True, null=True)
    railuk_manufacturer_code = models.CharField(
        max_length=3, blank=True, null=True)
    brd_manufacturer_code = models.CharField(
        max_length=3, blank=True, null=True)
    brsl_manufacturer_code = models.CharField(
        max_length=10, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    pre_grouping_owner = models.CharField(
        max_length=10, blank=True, default='')  # pre1923
    grouping_owner = models.CharField(
        max_length=4, blank=True, default='')  # 1923-1947
    br_region_owner = models.CharField(
        max_length=3, blank=True, default='')  # 1948-1997
    date_opened = models.CharField(max_length=10, blank=True, null=True)
    date_closed = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=77, blank=True, null=True)
    steam = models.CharField(max_length=10, blank=True, null=True)
    diesel = models.CharField(max_length=10, blank=True, null=True)
    electric = models.CharField(max_length=10, blank=True, null=True)
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    lococlass_designed = models.ManyToManyField(
        LocoClass, through='ClassDesigner', related_name="manufacturer_designer")
    lococlass_built = models.ManyToManyField(
        LocoClass, through='ClassManufacturer', related_name="manufacturer_manufacturer")

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse
        return reverse('companies:manufacturer', kwargs={'manufacturer_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Manufacturers'


class ClassManufacturer(models.Model):
    lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
    manufacturer_fk = models.ForeignKey(
        Manufacturer, blank=True, null=True, on_delete=models.CASCADE)
    person_fk = models.ForeignKey(
        Person, blank=True, null=True, on_delete=models.CASCADE)
    company_fk = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.person_fk is not None:
            manufacturer = self.person_fk.name
        elif self.manufacturer_fk is not None:
            manufacturer = self.manufacturer_fk.name
        elif self.company_fk is not None:
            manufacturer = self.company_fk.name
        else:
            manufacturer = ""
        return f"{manufacturer}"


class ClassDesigner(models.Model):
    lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
    manufacturer_fk = models.ForeignKey(
        Manufacturer, blank=True, null=True, on_delete=models.CASCADE)
    person_fk = models.ForeignKey(
        Person, blank=True, null=True, on_delete=models.CASCADE)
    company_fk = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.person_fk is not None:
            designer = self.person_fk.name
        elif self.manufacturer_fk is not None:
            designer = self.manufacturer_fk.name
        elif self.company_fk is not None:
            designer = self.company_fk.name
        else:
            designer = ""
        return f"{designer}"


class ClassOwnerOperator(models.Model):
    lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
    company_fk = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lococlass_fk} {self.company_fk}"
