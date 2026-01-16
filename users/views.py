from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import BootstrapUserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username,
                password=form.cleaned_data['password1']
            )
            login(request, authenticated_user)
            messages.success(request, "Your account has been created successfully!")
            return HttpResponseRedirect(reverse('mainmenu:index'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BootstrapUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
