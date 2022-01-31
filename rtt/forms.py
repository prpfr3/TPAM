from django import forms
from .models import NaPTANRailReferences

TIMETABLE_CHOICES = (
    ("Timetable",  "Timetable"), 
    ("RealTime Passenger", "RealTime Passenger"),  
    ("RealTime Freight", "RealTime Freight"),
)

class GetLocationForm(forms.ModelForm):
  class Meta:
    model = NaPTANRailReferences
    fields = ['stationname', 'atcocode', 'tiploccode', 'crscode', 'easting', 'northing']
    labels = {'stationname':'Station:-', 'atcocode':'ATCO code:-', 'tiploccode': 'TIPLOC code:-', 'crscode':'CRS code', 'easting':'OS Map Easting', 'northing': 'OS Map Northing'}

class ChooseLocationForm(forms.ModelForm):
  timetable_choice = forms.ChoiceField(choices=TIMETABLE_CHOICES)
  # crscode = forms.ModelChoiceField(queryset=NaPTANRailReferences.objects.all().order_by('stationname'))
  
  class Meta:
    model = NaPTANRailReferences
    fields = ('crscode', 'stationname')
    