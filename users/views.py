from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
  if request.method != 'POST':
    form = UserCreationForm()
  else:
    form = UserCreationForm(data=request.POST)

    if form.is_valid():
      new_user = form.save()
      authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
      login(request, authenticated_user)
      return HttpResponseRedirect(reverse('mainmenu:index'))

  context = {'form': form}
  return render(request, 'users/register.html', context)