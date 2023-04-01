from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import *

class LocoClassSelectionForm(forms.ModelForm):
    class Meta:
        model = LocoClassList
        fields = ('name',)

class LocomotiveSelectionForm(forms.ModelForm):
    class Meta:
        model = Locomotive
        fields = ('identifier',)

class LocoClassForm(forms.ModelForm):
    class Meta:
        model = LocoClass
        fields = ["wikiname", "br_power_class", "wheel_body_type"]
        labels = {'wikiname':'class', 'wheel_body_type':'wheel configuration',}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}