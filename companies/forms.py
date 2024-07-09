from django import forms
from .models import *


class CompanySelectionForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name",)


class ManufacturerSelectionForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ("name",)
