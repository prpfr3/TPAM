import contextlib
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import *
from .forms import MVImageForm, MVBMImageCreateForm

def index(request):
  return render(request, 'mvs/index.html')

def MVBMimage_create(request):
  if request.method == 'POST':
      form = MVBMImageCreateForm(data=request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          new_item = form.save(commit=False)
          new_item.user = request.user
          new_item.save()
          messages.success(request, 'Image added successfully')
          return redirect(new_item.get_absolute_url())
  else:
      form = MVBMImageCreateForm(data=request.GET)
      context = {'section': 'images', 'form': form}
      return render(request,'mvs/mvbmimage_new.html', context)

def military_vehicle_classes(request):
  military_vehicle_classes = MilitaryVehicleClass.objects.order_by('id')
  favorites = []
  if request.user.is_authenticated:
      rows = request.user.favorite_things.values('id')
      favorites = [ row['id'] for row in rows ]
  context = {'military_vehicle_classes': military_vehicle_classes, 'favorites': favorites}
  return render(request, 'mvs/military_vehicle_class_list.html', context)

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
      print("Add PK",pk)
      t = get_object_or_404(MilitaryVehicleClass, id=pk)
      fav = Fav(user=request.user, thing=t)
      with contextlib.suppress(IntegrityError):
        fav.save()  # In case of duplicate key
      return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
      print("Delete PK",pk)
      t = get_object_or_404(MilitaryVehicleClass, id=pk)
      with contextlib.suppress(Fav.DoesNotExist):
        fav = Fav.objects.get(user=request.user, thing=t).delete()
      return HttpResponse()

def military_vehicle_class(request, military_vehicle_class_id):
  military_vehicle_class = MilitaryVehicleClass.objects.get(id=military_vehicle_class_id)
  context = {'military_vehicle_class': military_vehicle_class}
  return render(request, 'mvs/military_vehicle_class.html', context)

def mvimages(request):
  mvimages = MVImage.objects.filter(location=7).order_by('image_name')
  paginator = Paginator(mvimages, 33)
  page = request.GET.get('page')
  try:
      mvimages = paginator.page(page)
  except PageNotAnInteger:
      mvimages = paginator.page(1)
  except EmptyPage:
      mvimages = paginator.page(paginator.num_pages)
  context = {'page': page, 'mvimages': mvimages}
  return render(request, 'mvs/mvimage_list.html', context)

def mvimage(request, mvimage_id):
  mvimage = MVImage.objects.get(id=mvimage_id)
  context = {'mvimage': mvimage}
  return render(request, 'mvs/mvimage.html', context)

@login_required
def new_mvimage(request):
  if request.method != 'POST':
    form = MVImageForm()
  else:
    form = MVImageForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('mvs:mvimages'))

  context = {'form': form}
  return render(request, 'mvs/mvimage_new.html', context)

@login_required
def edit_mvimage(request, mvimage_id):
  mvimage = MVImage.objects.get(id=mvimage_id)

  if request.method != 'POST':
    form = MVImageForm(instance=mvimage)
  else:
    form = MVImageForm(instance=mvimage, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('mvs:mvimage', args=[mvimage_id]))

  context = {'mvimage': mvimage,'form': form}
  return render(request, 'mvs/mvimage_edit.html', context)