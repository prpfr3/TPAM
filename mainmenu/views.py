from django.shortcuts import render
from .models import MyDjangoApp

def index(request):
  mydjangoapps = MyDjangoApp.objects.all()
  return render(request, 'mainmenu/index.html',{'mydjangoapps':mydjangoapps})