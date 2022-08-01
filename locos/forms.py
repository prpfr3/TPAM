from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from tinymce.widgets import TinyMCE

from .models import Person, Image, Company, Builder, LocoClass, Route, Slide, LocoClassList, UkAdminBoundaries, LocosRoutesGeoClosed, LocosRoutesGeoOsm

SLIDE_ORDER_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddSlideForm(forms.Form):
    slide_order = forms.TypedChoiceField(
                                choices=SLIDE_ORDER_CHOICES,
                                coerce=int)

class SlideSelectionForm(forms.ModelForm):

    class Meta:
        model = Slide
        fields = ('text_headline',)


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

class RouteSelectionForm(forms.ModelForm):

    class Meta:
        model = Route
        fields = ('name', 'wikipedia_route_categories')

class PersonForm(forms.ModelForm):
  class Meta:
    model = Person
    fields = ['name', 'wikitextslug', 'notes']
    labels = {'name':'', 'wikitextslug':'wikipedia slug', 'notes':''}
    widgets = {'text': forms.Textarea(attrs={'cols':80})}

class ImageForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image_name', 'image', 'location', 'visit', 'notes']
    labels = {'image_name':'Title', 'image':'Filename',  'location':'Location', 'visit':'Visit', 'notes':'Notes'}
    widgets = {'text': forms.Textarea(attrs={'cols':80})}

class LocoClassForm(forms.ModelForm):
 class Meta:
   model = LocoClass
   fields = ["wikipedia_name", "wikipedia_name", "br_power_class", "wheel_body_type"]
   labels = {'wikipedia_name':'class', 'wheel_body_type':'wheel configuration',}
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

class LocationChoiceField(forms.Form):
    #queryset=UkAdminBoundaries.objects.all().order_by('ctyua19nm'), #For selecting by county rather than route
    #queryset=LocosRoutesGeoClosed.objects.all().order_by('name')
    locations = forms.ModelChoiceField(
        queryset=UkAdminBoundaries.objects.all().order_by('ctyua19nm'),
        empty_label=None
    )

class LocationOSMChoiceField(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=LocosRoutesGeoOsm.objects.filter(type='route').order_by('name'),
        empty_label=None
    )
