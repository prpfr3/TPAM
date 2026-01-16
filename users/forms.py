from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class BootstrapUserCreationForm(UserCreationForm):
    """A user creation form with Bootstrap styling and required email field.
    
    This form customizes the default Django user creation form to include an email field and Bootstrap CSS classes.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )

    class Meta:
        model = User
        fields = ("username", "email")  # include email here!
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure password fields have form-control
        self.fields['password1'].widget.attrs.update({"class": "form-control", "placeholder": ""})
        self.fields['password2'].widget.attrs.update({"class": "form-control", "placeholder": ""})
        self.fields['username'].widget.attrs.update({"class": "form-control", "placeholder": ""})
