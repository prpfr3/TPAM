from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import Topic, Post, Reference
from locos.models import LocoClass
from companies.models import Company
from locations.models import Location, Route


class PostFilterForm(forms.Form):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(), required=False, empty_label="All topics"
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status", "url", "slug", "topic"]
        labels = {"title": "", "body": "", "status": "", "url": "url", "slug": "Slug"}
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Title"}
            ),
            "body": TinyMCE(
                attrs={"class": "form-control tinymce-editor", "cols": 80, "rows": 30}
            ),
            "status": forms.Select(
                attrs={"class": "form-control", "placeholder": "Enter Status"}
            ),
            "url": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter a URL (Optional)"}
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Auto-generated from title",
                }
            ),
        }


class ReferenceSelectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        if clear_previous_criteria := kwargs.pop("clear_previous_criteria", False):
            kwargs["initial"] = {
                "title": None,
                "year": None,
                "month": None,
                "authors": None,
                "editors": None,
                "journal": None,
                "volume": None,
                "issue": None,
            }

        super().__init__(*args, **kwargs)

    class Meta:
        model = Reference
        fields = (
            "title",
            "year",
            "month",
            "authors",
            "editors",
            "journal",
            "volume",
            "issue",
        )


class ReferenceAdminForm(forms.ModelForm):

    lococlasses = forms.ModelMultipleChoiceField(
        queryset=LocoClass.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Loco Classes", is_stacked=False),
    )

    companies = forms.ModelMultipleChoiceField(
        queryset=Company.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Companies", is_stacked=False),
    )

    routes = forms.ModelMultipleChoiceField(
        queryset=Route.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Routes", is_stacked=False),
    )

    locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Locations", is_stacked=False),
    )

    class Meta:
        model = Reference
        fields = "__all__"
        widgets = {
            "description": TinyMCE(
                attrs={"class": "form-control tinymce-editor", "cols": 80, "rows": 30}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["lococlasses"].initial = (
                self.instance.lococlass_references.all()
            )
            self.fields["companies"].initial = self.instance.company_references.all()
            self.fields["locations"].initial = self.instance.locations_references.all()
            self.fields["routes"].initial = self.instance.routes_references.all()

    def save(self, commit=True):
        # 1. Get the instance from the parent save method
        instance = super().save(commit=False)

        # 2. If we are committing, save the parent instance first to get an ID BEFORE setting M2M relationships
        if commit:
            instance.save()
            # 3. Now that the instance has an ID, we can set M2M relationships
            instance.lococlass_references.set(self.cleaned_data["lococlasses"])
            instance.company_references.set(self.cleaned_data["companies"])
            instance.locations_references.set(self.cleaned_data["locations"])
            instance.routes_references.set(self.cleaned_data["routes"])
        else:
            # 4. If commit=False (common in Admin), Django Admin expects 
            # a save_m2m() method to be added to the form.
            def save_m2m():
                instance.lococlass_references.set(self.cleaned_data["lococlasses"])
                instance.company_references.set(self.cleaned_data["companies"])
                instance.locations_references.set(self.cleaned_data["locations"])
                instance.routes_references.set(self.cleaned_data["routes"])
            
            self.save_m2m = save_m2m

        return instance
