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


class LocoClassSelectionForm(forms.ModelForm):
    designer_person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    owner_operators = forms.ModelChoiceField(
        queryset=Company.objects.order_by("name"),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    manufacturers = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    wheel_arrangement = forms.ModelChoiceField(
        queryset=WheelArrangement.objects.all(),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    class Meta:
        model = LocoClass
        fields = (
            "name",
            "designer_person",
            "owner_operators",
            "manufacturers",
            "wheel_arrangement",
            "power_type",
        )

        labels = {
            "name": "Name",
            "designer_person": "Designer",
            "owner_operators": "Owner Operator",
            "manufacturers": "Manufacturer",
            "wheel_arrangement": "Wheel Arrangements",
            "power_type": "Traction Type (Steam, Diesel, Electric)",
        }


class LocomotiveSelectionForm(forms.ModelForm):
    class Meta:
        model = Locomotive
        fields = ("number_as_built",)

        widgets = {
            "number_as_built": forms.TextInput(
                attrs={
                    "style": "width: 100px",
                }
            )
        }


class LocomotiveImageForm(forms.ModelForm):
    heritage_site = forms.ModelChoiceField(
        queryset=HeritageSite.objects.order_by("name"),
        required=False,
        widget=Select2Widget(
            attrs={"class": "search-select2", "style": "width: 200px;"}
        ),
    )

    class Meta:
        model = Image
        fields = ("image_name", "heritage_site")
        labels = {"image_name": "Title", "heritage_site": "Heritage Site"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_name"].required = (
            False  # For this form override the model mandatory status
        )
