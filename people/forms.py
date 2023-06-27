from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *


class PersonSelectionForm(forms.ModelForm):
    birthyear = forms.CharField(label="Birth Year", max_length=4, required=False)
    diedyear = forms.CharField(label="Year Died", max_length=4, required=False)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        if clear_previous_criteria := kwargs.pop("clear_previous_criteria", False):
            kwargs["initial"] = {
                "name": None,
                "birthyear": None,
                "diedyear": None,
            }

        super().__init__(*args, **kwargs)
        self.fields["role"].queryset = Role.objects.order_by("role")

    class Meta:
        model = Person
        fields = ("name",)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "wikitextslug"]
        labels = {
            "name": "",
            "wikitextslug": "wikipedia slug",
        }
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}
