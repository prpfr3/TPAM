from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger

from .models import AircraftClass, AirImage, AirBMImage
from .forms import AirImageForm, AirBMImageCreateForm

def index(request):
  return render(request, 'aircraft/index.html')

def AirBMimage_create(request):
  if request.method == 'POST':
      # form is sent
      form = AirBMImageCreateForm(data=request.POST)
      if form.is_valid():
          cd = form.cleaned_data
          new_item = form.save(commit=False)

          # assign current user to the item
          new_item.user = request.user
          new_item.save()
          messages.success(request, 'Image added successfully')

          # redirect to new created item detail view
          return redirect(new_item.get_absolute_url())
  else:
      # build form with data provided by the bookmarklet via GET
      form = AirBMImageCreateForm(data=request.GET)
      context = {'section': 'images', 'form': form}
      return render(request,'aircraft/airbmimage_new.html', context)

def aircraft_classes(request):
  aircraft_classes = AircraftClass.objects.order_by('id')
  context = {'aircraft_classes': aircraft_classes}
  return render(request, 'aircraft/aircraft_class_list.html', context)

def aircraft_class(request, aircraft_class_id):
  aircraft_class = AircraftClass.objects.get(id=aircraft_class_id)
  context = {'aircraft_class': aircraft_class}
  return render(request, 'aircraft/aircraft_class.html', context)

def airimages(request):
  airimages = AirImage.objects.order_by('image_name')
  paginator = Paginator(airimages, 20) # 3 posts in each page
  page = request.GET.get('page')
  try:
      airimages = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer deliver the first page
      airimages = paginator.page(1)
  except EmptyPage:
      # If page is out of range deliver last page of results
      airimages = paginator.page(paginator.num_pages)
  context = {'page': page, 'airimages': airimages}
  return render(request, 'aircraft/airimage_list.html', context)

def airimage(request, airimage_id):
  airimage = AirImage.objects.get(id=airimage_id)
  context = {'airimage': airimage}
  return render(request, 'aircraft/airimage.html', context)

@login_required
def new_airimage(request):
  if request.method != 'POST':
    form = AirImageForm()
  else:
    form = AirImageForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('aircraft:airimages'))

  context = {'form': form}
  return render(request, 'aircraft/airimage_new.html', context)

@login_required
def edit_airimage(request, airimage_id):
  airimage = AirImage.objects.get(id=airimage_id)

  if request.method != 'POST':
    form = AirImageForm(instance=airimage)
  else:
    form = AirImageForm(instance=airimage, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('aircraft:airimage', args=[airimage_id]))

  context = {'airimage': airimage,'form': form}
  return render(request, 'aircraft/airimage_edit.html', context)

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'aircraft/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'aircraft/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'aircraft/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )