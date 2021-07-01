from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('mainmenu:index'))

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

