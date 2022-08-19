from django.shortcuts import render

def index(request):
  return render(request, 'D3/index_static.html')
