from django import forms
from .models import *


class BRMPlansSelect(forms.ModelForm):

    class Meta:
        model = BRMPlans
        fields = ("archivenumber", "location", "description")
        labels = {
            "archivenumber": "Reference",
            "location": "Location",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["archivenumber"].required = (
            False  # For this form override the model mandatory status
        )
