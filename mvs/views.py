from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import HeritageSite, MilitaryVehicleClass, MVImage, Visit, MVBMImage, Fav
from .forms import MVImageForm, MVBMImageCreateForm

def index(request):
  return render(request, 'mvs/index.html')

def MVBMimage_create(request):
  if request.method == 'POST':
      # form is sent
      form = MVBMImageCreateForm(data=request.POST)
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
      form = MVBMImageCreateForm(data=request.GET)
      context = {'section': 'images', 'form': form}
      return render(request,'mvs/mvbmimage_new.html', context)

def military_vehicle_classes(request):
  military_vehicle_classes = MilitaryVehicleClass.objects.order_by('id')
  favorites = list()
  if request.user.is_authenticated:
      # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
      rows = request.user.favorite_things.values('id')
      # favorites = [2, 4, ...] using list comprehension
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
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(MilitaryVehicleClass, id=pk)
        fav = Fav(user=request.user, thing=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(MilitaryVehicleClass, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, thing=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()





def military_vehicle_class(request, military_vehicle_class_id):
  military_vehicle_class = MilitaryVehicleClass.objects.get(id=military_vehicle_class_id)
  context = {'military_vehicle_class': military_vehicle_class}
  return render(request, 'mvs/military_vehicle_class.html', context)

def mvimages(request):
  mvimages = MVImage.objects.order_by('image_name')
  paginator = Paginator(mvimages, 20) # 3 posts in each page
  page = request.GET.get('page')
  try:
      mvimages = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer deliver the first page
      mvimages = paginator.page(1)
  except EmptyPage:
      # If page is out of range deliver last page of results
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

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'mvs/index.html',
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
        'mvs/contact.html',
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
        'mvs/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )