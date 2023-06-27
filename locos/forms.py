from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import *


class SingleSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)
        self.attrs["size"] = 1  # Display only one option


class LocoClassSelectionForm(forms.ModelForm):
    # STRING SEARCH BELOW FAVOURED OVER THIS DROP DOWN SEARCH
    # name = forms.ModelChoiceField(
    #     queryset=LocoClassList.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={"class": "search-select2"}),
    # )

    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "search-input"})
    )

    designer_person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select2"}),
    )

    owner_operators = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select2"}),
    )

    manufacturers = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "search-select2"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["name"].queryset = LocoClassList.objects.order_by("name")

        # STRING SEARCH BELOW FAVOURED OVER THIS DROP DOWN SEARCH
        self.fields["name"].label = "Class Name"  # Optional: Customize the field label

    def clean_name(self):
        if name := self.cleaned_data.get("name"):
            return LocoClassList.objects.filter(name__icontains=name)
        return LocoClassList.objects.all()

    class Meta:
        model = LocoClass
        fields = (
            "wheel_body_type",
            "wheel_arrangement",
            "designer_person",
            "owner_operators",
            "manufacturers",
        )
        widgets = {
            "wheel_body_type": forms.Select(attrs={"class": "search-select2"}),
            "wheel_arrangement": forms.Select(attrs={"class": "search-select2"}),
            "designer_person": forms.Select(attrs={"class": "search-select2"}),
            "owner_operators": forms.Select(attrs={"class": "search-select2"}),
            "manufacturers": forms.Select(attrs={"class": "search-select2"}),
        }
        labels = {
            "wheel_body_type": "Type",
            "wheel_arrangement": "Wheel Arrangement",
            "designer_person": "Designer",
            "owner_operators": "Owner Operator",
            "manufacturers": "Manufacturer",
        }


class LocomotiveSelectionForm(forms.ModelForm):
    class Meta:
        model = Locomotive
        fields = ("identifier",)


class LocoClassForm(forms.ModelForm):
    class Meta:
        model = LocoClass
        fields = ["wikiname", "power_class", "wheel_body_type"]
        labels = {
            "wikiname": "class",
            "power_class": "power class",
            "wheel_body_type": "wheel configuration",
        }
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
