from django import forms
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import *

class BuilderSelectionForm(forms.ModelForm):
    class Meta:
        model = Builder
        fields = ('name',)

class CompanySelectionForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

class PersonSelectionForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name',)

class LocoClassSelectionForm(forms.ModelForm):
    class Meta:
        model = LocoClassList
        fields = ('name',)

class LocomotiveSelectionForm(forms.ModelForm):
    class Meta:
        model = Locomotive
        fields = ('identifier',)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'wikitextslug']
        labels = {'name':'', 'wikitextslug':'wikipedia slug',}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}

class LocoClassForm(forms.ModelForm):
    class Meta:
        model = LocoClass
        fields = ["wikiname", "br_power_class", "wheel_body_type"]
        labels = {'wikiname':'class', 'wheel_body_type':'wheel configuration',}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}