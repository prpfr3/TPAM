from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from .models import Post, Topic, Reference
from urllib import request

# from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


"""class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
"""


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'url']
        labels = {'title': '', 'body': '', 'status': '', 'url': 'url'}
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 50}),
            'title': forms.TextInput(attrs={'class': 'form-control', "placeholder": ".form-control-lg"}),
            #  'body': forms.Textarea(attrs={'class': 'form-control', "placeholder" : ".form-control-md"}),
            'status': forms.Select(attrs={'class': 'form-control', "placeholder": ".form-control-sm"}),
            'url': forms.TextInput(attrs={'class': 'form-control', "placeholder": ".form-control-lg"}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class ReferenceSelectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        if clear_previous_criteria := kwargs.pop('clear_previous_criteria', False):
            kwargs['initial'] = {
                'title': None,
                'year': None,
                'month': None,
                'authors': None,
                'editors': None,
                'journal': None,
                'volume': None,
                'issue': None,
            }

        super().__init__(*args, **kwargs)

    class Meta:
        model = Reference
        fields = ('title', 'year', 'month',
                  'authors', 'editors', 'journal', 'volume', 'issue')
