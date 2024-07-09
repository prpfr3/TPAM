from django import forms
from django.utils.translation import gettext_lazy as _
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import MVImage, MVBMImage, MilitaryVehicleClass


class MilitaryVehicleClassSelectionForm(forms.ModelForm):
    class Meta:
        model = MilitaryVehicleClass
        fields = ('mvclass',)
        labels = {'mvclass': 'Class'}
        widgets = {
            'url': forms.HiddenInput,  # Will be hidden as url grabbed by JS
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not '
                                        'match valid image extensions.')
        return url

    # Override the model form save process to handle the url before saving (as an alternative could also use different code to this in the view)
    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        image = super(MVBMImageCreateForm, self).save(commit=False)
        # Get the url from the cleaned_data dictionary
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)
        # Save the field 'image' which is an ImageField, of the image instance. It will be put in the media directory
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image


class MVImageForm(forms.ModelForm):
    class Meta:
        model = MVImage
        fields = ['image_name', 'image', 'mvclass', 'location', 'notes']
        labels = {'image_name': 'Title', 'image': 'Filename',
                  'mvclass': 'Military Vehicle Class', 'location': 'Location', 'notes': 'Notes'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
