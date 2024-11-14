from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from .models import *


class Select2Widget(forms.Select):
    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css",
            )
        }
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js",
        )

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs)
        script = """
            <script>
                $(document).ready(function() {{
                    $('#id_{name}').select2({{
                        placeholder: 'Select an option',
                        allowClear: true
                    }});
                }});
            </script>
        """.format(
            name=name
        )
        return mark_safe(output + script)


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
        labels = {"itemAltLabel": "ELR code:-", "itemLabel": "ELR description:-"}


TYPES = (
    ("Closed", "Closed Station"),
    ("Current", "Current Station"),
)


class LocationSelectionForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
        queryset=LocationCategory.objects.all(), required=False, label="Categories"
    )

    def __init__(self, *args, **kwargs):
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

    owner_operators = forms.ModelChoiceField(
        queryset=Company.objects.order_by("name"),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    categories = forms.ModelChoiceField(
        queryset=RouteCategory.objects.order_by("category"),
        required=False,
        label="Categories",
        widget=Select2Widget(
            attrs={
                "class": "search-select2",
                "style": "width: 200px;",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Route Name"
        self.fields["owner_operators"].label = "Company"

    class Meta:
        model = Route
        fields = ("name", "owner_operators", "categories")

        labels = {
            "name": "Route Name",
            "owner_operators": "Company",
            "categories": "Categories",
        }


# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = [
#             "wikiname",
#             "postcode",
#             "opened",
#             "closed",
#             "atcocode",
#             "tiploccode",
#             "crscode",
#             "easting",
#             "northing",
#             "slug",
#         ]
#         labels = {
#             "wikiname": "Name",
#             "postcode": "Postcode",
#             "opened": "Opened",
#             "closed": "Closed",
#             "atcocode": "ATCO code",
#             "tiploccode": "Tiploc code",
#             "crscode": "CRS code",
#             "easting": "Easting",
#             "northing": "Northing",
#             "slug": "Slug",
#         }
