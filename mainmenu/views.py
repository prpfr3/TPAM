from django.shortcuts import render
from .models import MyDjangoApp

def index(request):
  mydjangoapps = MyDjangoApp.objects
  return render(request, 'mainmenu/index.html',{'mydjangoapps':mydjangoapps})

#def motorvehicles(request):
#  mydjangoapps = MyDjangoApp.objects
#  return render(request, 'mainmenu/motorvehicles.html',{'mydjangoapps':mydjangoapps})