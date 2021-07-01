from django import forms
from .models import UKLicensedVehicles

class VehicleSelectionForm(forms.ModelForm):

    class Meta:
        model =UKLicensedVehicles
        fields = ('type', 'make', 'model', 'variant')