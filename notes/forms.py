from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from .models import Post, Topic
from urllib import request

#from .models import Comment

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
    labels = {'title':'', 'body':'', 'status':'', 'url':'url'}
    widgets = {
               'body': TinyMCE(attrs={'cols': 80, 'rows': 50}), 
               'title': forms.TextInput(attrs={'class': 'form-control', "placeholder" : ".form-control-lg"}),
              #  'body': forms.Textarea(attrs={'class': 'form-control', "placeholder" : ".form-control-md"}),
               'status': forms.Select(attrs={'class': 'form-control', "placeholder" : ".form-control-sm"}),
               'url': forms.TextInput(attrs={'class': 'form-control', "placeholder" : ".form-control-lg"}),
               }

class TopicForm(forms.ModelForm):
  class Meta:
    model = Topic
    fields = ['text']
    labels = {'text':''}