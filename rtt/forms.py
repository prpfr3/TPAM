from django import forms
from .models import NaPTANRailReferences

TIMETABLE_CHOICES = (
    ("Timetable", "Timetable"),
    ("RealTime Passenger", "RealTime Passenger"),
    ("RealTime Freight", "RealTime Freight"),
)


class LocationForm(forms.ModelForm):
    class Meta:
        model = NaPTANRailReferences
        fields = ["atcocode", "tiploccode", "crscode", "easting", "northing"]
        labels = {
            "atcocode": "ATCO code:-",
            "tiploccode": "TIPLOC code:-",
            "crscode": "CRS code",
            "easting": "OS Map Easting",
            "northing": "OS Map Northing",
        }
