from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from tinymce.widgets import TinyMCE

from .models import Post, Topic, Reference

# from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


"""class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
"""


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status", "url", "slug"]
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


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["text"]
        labels = {"text": ""}


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
