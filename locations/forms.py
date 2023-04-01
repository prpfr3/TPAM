from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *

class LocationChoiceField(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=UkAdminBoundaries.objects.filter(ctyua19cd__startswith='E').order_by('ctyua19nm'),
        empty_label=None
    )

class LocationOSMChoiceField(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=RouteGeoOsm.objects.filter(type='route').order_by('name'),
        empty_label=None
    )

class OSMRailMapSelectForm(forms.ModelForm):
  class Meta:
        model = ELR
        fields = ['itemAltLabel', 'itemLabel']
        labels = {'itemAltLabel':'ELR code:-', 'itemLabel':'Label:-'}

TYPES = (
    ("Closed", "Closed Station"),
    ("Current", "Current Station"),
)

class LocationSelectionForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('type', 'wikiname')
        labels = {'type':'Type','wikiname':'Name'}

class RouteSelectionForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('name', 'wikipedia_route_categories', 'source')

class LocationForm(forms.ModelForm):
  class Meta:
    model = Location
    fields = ['wikiname', 'type', 'postcode', 'opened', 'closed',
    'atcocode', 'tiploccode', 'crscode', 'easting', 'north']
    fields = {'wikiname':'Name', 'type':'Status', 'postcode':'Postcode', 'opened':'Opened', 'closed':'Closed',
    'atcocode':'ATCO code', 'tiploccode':'Tiploc code', 'crscode': 'CRS code', 'easting':'Easting', 'northing':'Northing'}