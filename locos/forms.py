from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from tinymce.widgets import TinyMCE

from .models import Person, Image, Company, Builder, LocoClass
from urllib import request

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
        model = LocoClass
        fields = ('grouping_company', 'pre_grouping_company', 'grouping_class',)

class PersonForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = ['name', 'wikitextslug', 'notes']
    labels = {'name':'', 'wikitextslug':'wikipedia slug', 'notes':''}
    widgets = {'text': forms.Textarea(attrs={'cols':80})}

class ImageForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image_name', 'image', 'location', 'notes']
    labels = {'image_name':'Title', 'image':'Filename',  'location':'Location', 'notes':'Notes'}
    widgets = {'text': forms.Textarea(attrs={'cols':80})}

class LocoClassForm(forms.ModelForm):
 class Meta:
   model = LocoClass
   fields = ["grouping_company", "pre_grouping_company", "grouping_class", "pre_grouping_class", "br_power_class", "wheel_body_type"]
   labels = {'grouping_company':'Grouping Company', 'pre_grouping_company':'company',
     'grouping_class':'class', 'wheel_body_type':'wheel configuration',}
   widgets = {'text': forms.Textarea(attrs={'cols':80})}

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
