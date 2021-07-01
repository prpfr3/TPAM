from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.text import slugify
from tinymce.widgets import TinyMCE

from .models import Post, Topic, UkAdminBoundaries
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

class LocationChoiceField(forms.Form):
    locations = forms.ModelChoiceField(
        queryset=UkAdminBoundaries.objects.all().order_by('ctyua19nm'),
        empty_label=None
    )

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'body', 'status', 'url']
    labels = {'title':'', 'body':'', 'status':'', 'url':'url'}
    widgets = {'body': TinyMCE(attrs={'cols': 80})}

class TopicForm(forms.ModelForm):
  class Meta:
    model = Topic
    fields = ['text']
    labels = {'text':''}

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254, widget=forms.TextInput({
                        'class': 'form-control',
                        'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput({
                        'class': 'form-control',
                        'placeholder':'Password'}))