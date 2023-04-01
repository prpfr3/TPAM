from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *

class PersonSelectionForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'role', 'source')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'wikitextslug']
        labels = {'name':'', 'wikitextslug':'wikipedia slug',}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}