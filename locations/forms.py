from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.gis.geos import Point
from tinymce.widgets import TinyMCE
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



class LocationAdminForm(forms.ModelForm):
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)

    class Meta:
        model = Location
        fields = "__all__"

        widgets = {
            "notes": TinyMCE(
                attrs={"class": "form-control tinymce-editor", "cols": 80, "rows": 30}
            ),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing an existing record, prefill lat/lon from geometry
        if self.instance and self.instance.geometry:
            point = self.instance.geometry
            self.fields["latitude"].initial = point.y
            self.fields["longitude"].initial = point.x

    def clean(self):
        cleaned = super().clean()

        lat = cleaned.get("latitude")
        lon = cleaned.get("longitude")

        if lat is not None and lon is not None:
            if not (-90 <= lat <= 90):
                self.add_error("latitude", "Latitude must be between -90 and 90.")
            if not (-180 <= lon <= 180):
                self.add_error("longitude", "Longitude must be between -180 and 180.")

            cleaned["geometry"] = Point(lon, lat)

        return cleaned
    
