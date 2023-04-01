from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import *

class CompanySelectionForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

class ManufacturerSelectionForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ('name',)