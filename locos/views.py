from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Engineer, Image, ModernClass
from .forms import EngineerForm, ImageForm

def index(request):
  return render(request, 'locos/index.html')

def engineers(request):
  engineers = Engineer.objects.order_by('eng_name')
  context = {'engineers': engineers}
  return render(request, 'locos/engineer_list.html', context)


def engineer(request, engineer_id):
  engineer = Engineer.objects.get(id=engineer_id)
  context = {'engineer': engineer}
  return render(request, 'locos/engineer.html', context)


@login_required
def new_engineer(request):
  if request.method != 'POST':
    form = EngineerForm()
  else:
    form = EngineerForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:engineers'))

  context = {'form': form}
  return render(request, 'locos/engineer_new.html', context)


@login_required
def edit_engineer(request, engineer_id):
  engineer = Engineer.objects.get(id=engineer_id)

  if request.method != 'POST':
    form = EngineerForm(instance=engineer)
  else:
    form = EngineerForm(instance=engineer, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:engineer', args=[engineer_id]))

  context = {'engineer': engineer,'form': form}
  return render(request, 'locos/engineer_edit.html', context)

def loco_classes(request):
  loco_classes = LocoClass.objects.order_by('grouping_company', 'pre_grouping_company', 'grouping_class')
  context = {'loco_classes': loco_classes}
  return render(request, 'locos/loco_class_list.html', context)


def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  context = {'loco_class': loco_class}
  return render(request, 'locos/loco_class.html', context)


def modern_classes(request):
  modern_classes = ModernClass.objects.order_by('modern_class')
  context = {'modern_classes': modern_classes}
  return render(request, 'locos/modern_class_list.html', context)


def modern_class(request, modern_class_id):
  modern_class = ModernClass.objects.get(id=modern_class_id)
  context = {'modern_class': modern_class}
  return render(request, 'locos/modern_class.html', context)


def images(request):
  images = Image.objects.order_by('image_name')
  paginator = Paginator(images, 20) 
  page = request.GET.get('page')
  try:
      images = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer deliver the first page
      images = paginator.page(1)
  except EmptyPage:
      # If page is out of range deliver last page of results
      images = paginator.page(paginator.num_pages)
  context = {'page': page, 'images': images}
  return render(request, 'locos/image_list.html', context)


def image(request, image_id):
  image = Image.objects.get(id=image_id)
  context = {'image': image}
  return render(request, 'locos/image.html', context)


@login_required
def new_image(request):
  if request.method != 'POST':
    form = ImageForm()
  else:
    form = ImageForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:images'))

  context = {'form': form}
  return render(request, 'locos/image_new.html', context)


@login_required
def edit_image(request, image_id):
  image = Image.objects.get(id=image_id)

  if request.method != 'POST':
    form = ImageForm(instance=image)
  else:
    form = ImageForm(instance=image, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:image', args=[image_id]))

  context = {'image': image,'form': form}
  return render(request, 'locos/image_edit.html', context)

def home(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'locos/index.html',{'title':'Home Page', 'year':datetime.now().year,})


def contact(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'locos/contact.html', {'title':'Contact', 'message':'Your contact page.', 'year':datetime.now().year,})


def about(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'locos/about.html', {'title':'About', 'message':'Your application description page.','year':datetime.now().year,})