from django import forms
from .models import NaPTANRailReferences

class GetLocationForm(forms.ModelForm):
  class Meta:
    model = NaPTANRailReferences
    fields = ['stationname', 'atcocode', 'tiploccode', 'crscode', 'easting', 'northing']
    labels = {'stationname':'Station:-', 'atcocode':'ATCO code:-', 'tiploccode': 'TIPLOC code:-', 'crscode':'CRS code', 'easting':'OS Map Easting', 'northing': 'OS Map Northing'}

class ChooseLocationForm(forms.ModelForm):
  class Meta:
    model = NaPTANRailReferences
    fields = ['crscode']
    