from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *


class RegionChoiceForm(forms.Form):
    regions = forms.ModelChoiceField(
        queryset=UKArea.objects.order_by("ITL121NM"),
        empty_label=None,
    )


class LocationOSMChoiceField(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=RouteGeoOsm.objects.filter(type="route").order_by("name"),
        empty_label=None,
    )


class ELRSelectForm(forms.ModelForm):
    class Meta:
        model = ELR
        fields = ["itemAltLabel", "itemLabel"]
        labels = {"itemAltLabel": "ELR code:-", "itemLabel": "Label:-"}


TYPES = (
    ("Closed", "Closed Station"),
    ("Current", "Current Station"),
)


class LocationSelectionForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
        queryset=LocationCategory.objects.all(), required=False, label="Categories"
    )

    def __init__(self, *args, **kwargs):
        if clear_previous_criteria := kwargs.pop("clear_previous_criteria", False):
            kwargs["initial"] = {
                "name": None,
            }

        super().__init__(*args, **kwargs)

        self.fields["categories"].queryset = LocationCategory.objects.order_by(
            "category"
        )

    class Meta:
        model = Location
        fields = ["name"]
        labels = {"name": "Name"}


class RouteSelectionForm(forms.ModelForm):
    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "search-input"})
    )

    owner_operators = forms.ModelMultipleChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "search-select2"}),
    )

    categories = forms.ModelChoiceField(
        queryset=RouteCategory.objects.all(), required=False, label="Categories"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Route Name"
        self.fields["owner_operators"].label = "Company"

    class Meta:
        model = Route
        fields = ("name", "owner_operators", "categories")

        widgets = {
            "owner_operators": forms.SelectMultiple(attrs={"class": "search-select2"}),
            "categories": forms.Select(attrs={"class": "search-select2"}),
        }

        labels = {
            "name": "Route Name",
            "owner_operators": "Company",
            "categories": "Categories",
        }


class RouteSectionSelectionForm(forms.ModelForm):
    class Meta:
        model = RouteSection
        fields = [
            "name",
        ]
        labels = {
            "name": "name",
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "wikiname",
            "postcode",
            "opened",
            "closed",
            "atcocode",
            "tiploccode",
            "crscode",
            "easting",
            "northing",
        ]
        labels = {
            "wikiname": "Name",
            "postcode": "Postcode",
            "opened": "Opened",
            "closed": "Closed",
            "atcocode": "ATCO code",
            "tiploccode": "Tiploc code",
            "crscode": "CRS code",
            "easting": "Easting",
            "northing": "Northing",
        }
