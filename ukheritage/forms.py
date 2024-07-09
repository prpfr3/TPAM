from django import forms
from .models import GdUkListedBuildings, MyPlaces
from locations.models import UkAdminBoundaries

LISTED_GRADES = (("I", "I"), ("II*", "II*"))

MAP_OR_LIST = (("Map", "Map Display"), ("List", "Tabular List"))


class ListedBuildingsSelectionForm(forms.ModelForm):
    address = forms.CharField(required=False)
    longitude = forms.FloatField(required=False)
    latitude = forms.FloatField(required=False)
    grades = forms.MultipleChoiceField(required=False, choices=LISTED_GRADES)
    map_or_list = forms.ChoiceField(
        choices=MAP_OR_LIST, initial="Map", widget=forms.RadioSelect
    )
    max_items = forms.IntegerField(required=False, initial=20)
    max_distance_kms = forms.FloatField(required=False, initial=100)

    class Meta:
        model = GdUkListedBuildings
        fields = (
            "id",
            "location",
            "name",
        )


class ListedBuildingForm(forms.ModelForm):

    # Only need to specify the field details if NOT using Crispy forms. form-control is a bootstrap class
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # mynotes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))

    class Meta:
        model = GdUkListedBuildings
        fields = (
            "name",
            "mynotes",
        )


class MyplacesForm(forms.ModelForm):

    # Only need to specify the field details if NOT using Crispy forms. form-control is a bootstrap class
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # mynotes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))

    class Meta:
        model = MyPlaces
        fields = ("name", "mynotes", "hyperlink", "wikislug")


class CountySelectForm(forms.Form):
    counties = forms.ModelChoiceField(
        queryset=UkAdminBoundaries.objects.filter(ctyua19cd__startswith="E").order_by(
            "ctyua19nm"
        ),
        empty_label=None,
    )
