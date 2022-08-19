import json
from sqlalchemy import null
import wikipediaapi
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpRequest, HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.db.models import Q, F, ExpressionWrapper, fields
from django.db.models import Count
from django.db.models.functions import ExtractYear

from .forms import *
from .models import *
from .storymap_cart import Cart

@require_POST
def cart_add(request, slide_id):
    cart = Cart(request)
    slide = get_object_or_404(Slide, id=slide_id)
    form = CartAddSlideForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(slide=slide,
                 slide_order=cd['slide_order'])
    else:
        print(" form not valid ", form.errors)
    return redirect('locos:cart_detail')


@require_POST
def cart_remove(request, slide_id):
    cart = Cart(request)
    slide = get_object_or_404(Slide, id=slide_id)
    cart.remove(slide)
    return redirect('locos:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['update_slide_order_form'] = CartAddSlideForm(initial={'slide_order': item['slide_order'],})

    return render(request, 'locos/cart_detail.html', {'cart': cart})


def slides(request):

    if request.method == 'POST':
        selection_criteria = SlideSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['text_headline'] != None:
            queryset = Slide.objects.filter(text_headline__icontains=selection_criteria.cleaned_data['text_headline']).order_by('text_headline')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Slide.objects.order_by('text_headline')
    else:
        selection_criteria = SlideSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Slide.objects.order_by('text_headline')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'slide_list': queryset}
    return render(request, 'locos/slide_list.html', context)

def slide(request, slide_id):
  slide = Slide.objects.get(id=slide_id)
  cart_slide_form = CartAddSlideForm()
  context = {'slide': slide, 'cart_slide_form':cart_slide_form}
  return render(request, 'locos/slide.html', context)


def index(request):
  return render(request, 'locos/index.html')

def persons(request):
    if request.method == 'POST':
        selection_criteria = PersonSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['name'] != None:
            queryset = Person.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Person.objects.order_by('name')
    else:
        selection_criteria = PersonSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Person.objects.order_by('name')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'person_list': queryset}
    return render(request, 'locos/person_list.html', context)

def storymap_references(request):
  references = Sighting.objects.order_by('id')

  storymap_dict = {"storymap":
      {"attribution": "",
        "call_to_action": True,
        "call_to_action_text": "",
        "map_as_image": False,
        "map_subdomains": "",
        "map_type": "osm:standard",
        "slides": [
            { "date": "",
              "location": {"line": True},
              "media": {"caption": "", "credit": "", "url": ""},
              "text": {"headline": "Steam Locomotive Picture Library", "text": ""},
              "type": "overview"
            },
        ],
        "zoomify": False
      }
    }

  forlooplimiter = 0

  for reference in references:

    if forlooplimiter < 13:
      forlooplimiter += 1

      slide_date = str(reference.DD) + "/" + str(reference.MM) + "/" + str(reference.YD) + str(reference.YY)
      slide_media_caption = str(reference.location_description) + " on " + str(reference.DD) + "/" + str(reference.MM) + "/" + str(reference.YD) + str(reference.YY)
      slide_media_credit = reference.citation + ' ' + reference.citation_specifics
      slide_headline = str(reference.location_description) + " on " + str(reference.DD) + "/" + str(reference.MM) + "/" + str(reference.YD) + str(reference.YY)

      #Turns a slugfield into a full url for the current site or keeps a url as is
      media_url = request.build_absolute_uri(reference.hyperlink)

      slide = {
        "background": {"url": ""},
        "date": slide_date,
        "location": {"lat": reference.northing, "line": True, "lon": reference.easting, "zoom": 12},
        "media": {"caption": slide_media_caption, "credit": slide_media_credit, "url": media_url},
        "text": {"headline": slide_headline, "text": reference.notes}
      }

      storymap_dict['storymap']['slides'].append(slide)

  storymap_json = json.dumps(storymap_dict)
  return render(request, 'locos/storymap_references.html', {'storymap_json':storymap_json})

def persons_timeline(request):
  persons = Person.objects.order_by('name')

  tdict = {
    "title": {
        "media": {
          "url": "",
          "caption": "",
          "credit": ""
        },
        "text": {
          "headline": "Railway Engineers Timeline",
          "text": "<p>Dates of Famous Engineers</p>"
        }
    },
    "events": [
    ]
  }

  forlooplimiter = 0

  for person in persons:

    if forlooplimiter < 4 and person.birthdate and person.dieddate:
      forlooplimiter += 1

      event = {
          "media": {
            "url": person.wikiimageslug,
            "caption": person.wikiimagetext,
            "credit": "Caption Credit: All credit to Wikipedia"
          },
          "start_date": {
            "year": person.birthdate[:4]
          },
          "end_date": {
            "year": person.dieddate[:4]
          },
          "text": {
            "headline": person.name,
            "text": person.notes
          }
        }

      tdict['events'].append(event)

  timeline_json = json.dumps(tdict)
  return render(request, 'locos/persons_timeline.html', {'timeline_json':timeline_json})

def persons_vis_timeline(request):
  persons = Person.objects.order_by('name')

  events = []
  forlooplimiter = 0

  for person in persons:

    if person.birthdate and person.dieddate:
      forlooplimiter += 1

      ## https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
      event = {
          "id": forlooplimiter,
          "content": person.name,
          "start": person.birthdate.replace("??", "01"), #Replace any unknown part of the date with 01 as vis_timeline requires full date
          "end": person.dieddate.replace("??", "01"),
          "event.type": 'point'
      }

      events.append(event)

  return render(request, 'locos/persons_vis_timeline.html', {'timeline_json':json.dumps(events)})

def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  context = {'loco_class': loco_class}
  return render(request, 'locos/loco_class.html', context)

@login_required
def new_loco_class(request):
  if request.method != 'POST':
    form = LocoClassForm()
  else:
    form = LocoClassForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:loco_classes'))

  context = {'form': form}
  return render(request, 'locos/loco_class_new.html', context)

@login_required
def edit_loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)

  if request.method != 'POST':
    form = LocoClassForm(instance=loco_class)
  else:
    form = LocoClassForm(instance=loco_class, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:loco_class', args=[loco_class_id]))

  context = {'loco_class': loco_class,'form': form}
  return render(request, 'locos/loco_class_edit.html', context)

def loco_classes(request):

    if request.method == 'POST':
        selection_criteria = LocoClassSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data != None:
            queryset = LocoClassList.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
            page = None
            context = {'selection_criteria':selection_criteria, 'errors': errors, 'page': page, 'loco_class_list': queryset}
            return render(request, 'locos/loco_class_list.html', context)
        else:
            errors = selection_criteria.errors or None
            queryset = LocoClassList.objects.order_by('name')
    else:
        selection_criteria = LocoClassSelectionForm()
        errors = selection_criteria.errors or None
        queryset = LocoClassList.objects.order_by('name')

    paginator = Paginator(queryset, 20)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'page': page, 'loco_class_list': queryset}
    return render(request, 'locos/loco_class_list.html', context)

def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  locomotives = Locomotive.objects.filter(lococlass=loco_class_id)
  references = Sighting.objects.filter(lococlass=loco_class_id)
  images = Image.objects.filter(lococlass=loco_class_id)
  operators = loco_class.company_owneroperator.all()
  class_designers1 = loco_class.person_designer.all()
  class_designers2 = loco_class.builder_designer.all()
  class_designers3 = loco_class.company_designer.all()
  class_builders1 = loco_class.person_builder.all()
  class_builders2 = loco_class.builder_builder.all()
  class_builders3 = loco_class.company_builder.all()

  wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
  page_name = loco_class.wikipedia_name.replace(' ', '_')
  wikipedia_summary = wiki_wiki.page(page_name).text

  context = {'loco_class':loco_class,
              'locomotives':locomotives,
              'operators':operators,
              'references':references,
              'images':images,
              'designers1':class_designers1,
              'designers2':class_designers2,
              'designers3':class_designers3,
              'builders1':class_builders1,
              'builders2':class_builders2,
              'builders3':class_builders3,
              'wikipedia_summary':wikipedia_summary,
  }

  return render(request, 'locos/loco_class.html', context)

def locomotives(request):

    if request.method == 'POST':
        selection_criteria = LocomotiveSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data != None:
            queryset = Locomotive.objects \
              .filter(identifier__icontains=selection_criteria.cleaned_data['identifier']) \
              .values('brd_class_name') \
              .annotate(total=Count('brd_class_name')) \
              .order_by('total')
            age = ExpressionWrapper(F('brd_withdrawn_date_datetime')-F('brd_build_date_datetime'), \
              output_field=fields.DurationField())
            queryset = Locomotive.objects \
              .filter(identifier__icontains=selection_criteria.cleaned_data['identifier']) \
              .annotate(age=age) \
              .order_by('age')
            errors = None
            context = {'selection_criteria':selection_criteria, 'errors': errors, 'locomotives_list': queryset}
            return render(request, 'locos/locomotives_list.html', context)
        else:
            errors = selection_criteria.errors or None
            queryset = Locomotive.objects.order_by('brd_number_as_built')
    else:
        selection_criteria = LocomotiveSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Locomotive.objects.order_by('brd_number_as_built')

    paginator = Paginator(queryset, 20)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'page': page, 'locomotives_list': queryset}
    return render(request, 'locos/locomotives_list.html', context)

def companies(request):
    if request.method == 'POST':
        selection_criteria = CompanySelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['name'] != None:
            queryset = Company.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Company.objects.order_by('name')
    else:
        selection_criteria = CompanySelectionForm
        errors = selection_criteria.errors or None
        queryset = Company.objects.order_by('name')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'company_list': queryset}
    return render(request, 'locos/company_list.html', context)

def routes(request):

    if request.method == 'POST':
        selection_criteria = RouteSelectionForm(request.POST)

        if selection_criteria.is_valid() and str(selection_criteria.cleaned_data['name']) != 'None':
            queryset = Route.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        elif selection_criteria.is_valid() and str(selection_criteria.cleaned_data['route_categories']) != 'None':
            queryset = Route.objects.filter(route_categories__in=selection_criteria.cleaned_data['route_categories']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Route.objects.order_by('name')
    else:
        selection_criteria = RouteSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Route.objects.order_by('name')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'route_list': queryset}
    return render(request, 'locos/route_list.html', context)

def company(request, company_id):
  company = Company.objects.get(id=company_id)
  wiki_categories = CompanyCategory.objects.filter(company=company_id)
  context = {'company': company, 'wiki_categories': wiki_categories}
  return render(request, 'locos/company.html', context)

def builders(request):

    if request.method == 'POST':
        selection_criteria = BuilderSelectionForm(request.POST)

        if selection_criteria.is_valid() and selection_criteria.cleaned_data['name'] != None:
            queryset = Builder.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            errors = None
        else:
            errors = selection_criteria.errors or None
            queryset = Builder.objects.order_by('name')
    else:
        selection_criteria = BuilderSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Builder.objects.order_by('name')

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'builder_list': queryset}
    return render(request, 'locos/builder_list.html', context)

def builder(request, builder_id):
  builder = Builder.objects.get(id=builder_id)
  context = {'builder': builder}
  return render(request, 'locos/manufacturer.html', context)

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
  loco_classes = LocoClass.objects.filter(image=image_id)
  context = {'image': image, 'loco_classes':loco_classes}
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

def routemap_folium(request, route_id):
    route = Route.objects.get(id=route_id)

    # First method for getting wikipedia data
    import wikipediaapi
    wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.HTML
    )
    slug = route.wikipedia_slug.replace('/wiki/', '')
    route_page = wiki_wiki.page(slug).text

    # Method 3:- Javascript. 
    # See template and https://stackoverflow.com/questions/26577292/is-there-a-way-to-embed-and-style-a-wikipedia-article-in-a-website
  
    # Generating the map
    import folium
    figure = folium.Figure()

    # A Wikipedia Route Page can have many Routemaps, though this is rarely if ever seen. But we select them all just in case.
    routemaps = route.wikipedia_routemaps.all()

    # Then for each routemap (though no known case of there being more than one for a route) we get all the route locations
    for routemap in routemaps:

      routelocations = RouteLocation.objects.filter(routemap_fk=routemap.id)
      # print(routelocations)
      for routelocation in routelocations:
        if routelocation.location_fk != None:
          # Start the folium map centering it on the geometry of the first route location which had geometry
          m = folium.Map([routelocation.location_fk.geometry.y, routelocation.location_fk.geometry.x], zoom_start= 13, tiles='cartodbpositron', prefer_canvas=True)
          m.add_to(figure)
          break

      # For each of the locations on the routemap, see if has a relationship with a location (i.e. a location is normally in the Routes table if it has a wikipedia page, normally for a railway station). Only if it has will there be geometry available which would allow us to add it to the map.
      for routelocation in routelocations:
        # print(routelocation.label, routelocation.location_fk)
        if routelocation.location_fk != None:
            # print(routelocation.location_fk.wikiname, routelocation.location_fk.geometry.y, routelocation.location_fk.geometry.x)
            # folium.GeoJson(data=routelocation.location_fk.geometry.geojson, popup=folium.Popup(str(routelocation.location_fk.wikiname),parse_html=True)).add_to(m)

            folium.Marker(location=[routelocation.location_fk.geometry.y, routelocation.location_fk.geometry.x], 
                       tooltip=str(routelocation.location_fk.wikiname), 
                       popup=folium.Popup(str(routelocation.location_fk.wikiname), parse_html=True)).add_to(m)

    figure.render()
    context =  {"map": figure, "route": route.name, "wikipage": route_page }
    return render(request, 'locos/routemap_folium.html', context)

def routemap(request, route_id):
    import markdown
    slide_list = []
    route = Route.objects.get(id=route_id)
    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict={}
    slide_dict['location_line'] = "true"
    slide_dict['media'] = {}
    slide_dict['media']['caption'] = ""
    slide_dict['media']['credit'] = ""
    slide_dict['media']['url'] = ""
    slide_dict['text'] = {}
    slide_dict['text']['headline'] = route.name
    slide_dict['text']['text'] = ""
    slide_dict['type'] = "overview"
    slide_list.append(slide_dict)

    routemaps = route.wikipedia_routemaps.all()
    for routemap in routemaps:
      routelocations = RouteLocation.objects.filter(routemap_fk=routemap.id)
      for routelocation in routelocations:
        if routelocation.location_fk != None:
          try:
            slide_dict={}
            slide_dict['background'] = {}
            slide_dict['background']['url'] = ""
            slide_dict['location'] = {}
            slide_dict['location']['lat'] = routelocation.location_fk.geometry.y
            slide_dict['location']['lon'] = routelocation.location_fk.geometry.x
            slide_dict['location']['zoom'] = "12"
            slide_dict['media'] = {}
            slide_dict['media']['caption'] = ""
            slide_dict['media']['credit'] = ""
            slide_dict['media']['url'] = ""
            slide_dict['text'] = {}
            slide_dict['text']['headline'] = routelocation.location_fk.wikiname

            html_string = markdown.markdown(routelocation.label.replace('/wiki/', 'https://en.wikipedia.org/wiki/'))
            slide_dict['text']['text'] = html_string.replace('"', '\'')
            slide_list.append(slide_dict)
          except:
            import sys
            e = sys.exc_info()[0]
            print(e)
            pass

      #Create a dictionary in the required JSON format, including the dictionary list of slides
      routemap_dict = {"storymap":
        {"attribution": "Paul Frost",
          "call_to_action": True,
          "call_to_action_text": "A Routemap",
          "map_as_image": False,
          "map_subdomains": "",
          "map_type": "osm:standard",
          "slides": slide_list,
          "zoomify": False
        }
      }

      storymap_json = json.dumps(routemap_dict)
      print(json.dumps(routemap_dict, sort_keys=False, indent=4))
      # Routemaps uses the same template as storymaps
    return render(request, 'locos/storymap.html', {'storymap_json':storymap_json})

def  storymaps(request):
    storymaps = SlideHeader.objects.order_by('text_headline')
    paginator = Paginator(storymaps, 20)
    page = request.GET.get('page')
    try:
        storymaps = paginator.page(page)
    except PageNotAnInteger:
        storymaps = paginator.page(1)
    except EmptyPage:
        storymaps = paginator.page(paginator.num_pages)
    context = {'page': page, 'storymaps': storymaps}
    return render(request, 'locos/storymaps.html', context)

def storymap(request, storymap_id):

    slide_list = []
    slideheader = SlideHeader.objects.get(id=storymap_id)
    slides = Slide.objects.filter(slideheader__id=storymap_id).order_by('slidepack__slide_order')

    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict={}
    slide_dict['location_line'] = slideheader.location_line
    slide_dict['media'] = {}
    slide_dict['media']['caption'] = slideheader.media_caption
    slide_dict['media']['credit'] = slideheader.media_credit
    slide_dict['media']['url'] = slideheader.media_url
    slide_dict['text'] = {}
    slide_dict['text']['headline'] = slideheader.text_headline
    slide_dict['text']['text'] = slideheader.text_text
    slide_dict['type'] = slideheader.type
    slide_list.append(slide_dict)

    #Add subsequent slides to the dictionary list from the Slide objects
    for slide in slides:
        slide_dict={}
        slide_dict['background'] = {}
        slide_dict['background']['url'] = slide.background
        slide_dict['location'] = {}
        slide_dict['location']['lat'] = slide.northing
        slide_dict['location']['lon'] = slide.easting
        slide_dict['location']['zoom'] = slide.zoom
        slide_dict['media'] = {}
        slide_dict['media']['caption'] = slide.media_caption
        slide_dict['media']['credit'] = slide.media_credit
        slide_dict['media']['url'] = slide.media_url
        slide_dict['text'] = {}
        slide_dict['text']['headline'] = slide.text_headline
        slide_dict['text']['text'] = slide.text_text
        slide_list.append(slide_dict)

    #Create a dictionary in the required JSON format, including the dictionary list of slides
    storymap_dict = {"storymap":
      {"attribution": "Paul Frost",
        "call_to_action": True,
        "call_to_action_text": "A Journey in Time",
        "map_as_image": False,
        "map_subdomains": "",
        "map_type": "osm:standard",
        "slides": slide_list,
        "zoomify": False
      }
    }

    storymap_json = json.dumps(storymap_dict)
    return render(request, 'locos/storymap.html', {'storymap_json':storymap_json})

def location_select(request):

    if request.method == 'POST':
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            county=str(selected_location)
            return HttpResponseRedirect(reverse('locos:map_closed_lines', args=[county]))
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {'location_list':location_list, 'errors': errors,}
        return render(request, 'locos/location_select.html', context)

class MapClosedLines(TemplateView):

    template_name = "locos/map_closed_lines.html"

    def get_context_data(self, **kwargs):
        county = self.kwargs['county_name']

        import os
        from sqlalchemy import create_engine, text
        from django.conf import settings
        import geopandas as gpd

        if os.environ.get('DATABASE_URL'):
            db_connection_url = os.environ.get('DATABASE_URL')
        else:
            db_connection_url = settings.DATABASE_URL
        con = create_engine(db_connection_url)

        # sql = text('SELECT * FROM public."UK_admin_boundaries" WHERE ctyua19nm = :county')      
        # county_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})
        # county_4326 = county_27700.to_crs(epsg=4326)
        # print(county_4326.head())

        """
        View originally constructed to select based on UK admin boundaries but the following throws an error when passed to gpd.GeoDataFrame
        sql = text('SELECT * FROM public."locos_routes_geo_closed" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        """
        sql = text('SELECT * FROM public."locos_routes_geo_closed" WHERE name = :county')
        sql = text('SELECT * FROM public."locos_routes_geo_closed"')    
        routes = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        import folium
        figure = folium.Figure()
        m = folium.Map([routes.geometry.centroid.y[0], routes.geometry.centroid.x[0]], zoom_start= 12, tiles='cartodbpositron', prefer_canvas=True)
        m.add_to(figure)
        folium.GeoJson(data=routes["geometry"], popup=routes["name"]).add_to(m)

        figure.render()
        return {"map": figure, "county": county}

def locationosm_select(request):

    if request.method == 'POST':
        location_list = LocationOSMChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            print(selected_location)
            county=str(selected_location)
            print(county)
            return HttpResponseRedirect(reverse('locos:map_osm_lines', args=[county]))
    else:
        location_list = LocationOSMChoiceField()
        errors = location_list.errors or None
        context = {'location_list':location_list, 'errors': errors,}
        return render(request, 'locos/locationosm_select.html', context)

class MapOSMLines(TemplateView):

    template_name = "locos/map_osm_lines.html"

    def get_context_data(self, **kwargs):
        county = self.kwargs['county_name']

        import os
        from sqlalchemy import create_engine, text
        from django.conf import settings
        import geopandas as gpd



        if os.environ.get('DATABASE_URL'):
            db_connection_url = os.environ.get('DATABASE_URL')
        else:
            db_connection_url = settings.DATABASE_URL
        con = create_engine(db_connection_url)

        # sql = text('SELECT * FROM public."UK_admin_boundaries" WHERE ctyua19nm = :county')      
        # county_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})
        # county_4326 = county_27700.to_crs(epsg=4326)
        # print(county_4326.head())

        """
        View originally constructed to select based on UK admin boundaries but the following throws an error when passed to gpd.GeoDataFrame
        sql = text('SELECT * FROM public."locos_routes_geo_closed" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        """
        sql = text('SELECT * FROM public."locos_routes_geo_osm" WHERE name = :county')    
        routes = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})


        import folium
        figure = folium.Figure()
        m = folium.Map([routes.geometry.centroid.y[0], routes.geometry.centroid.x[0]], zoom_start= 12, tiles='cartodbpositron', prefer_canvas=True)
        m.add_to(figure)
        folium.GeoJson(data=routes["geometry"], popup=routes["name"]).add_to(m)

        figure.render()
        return {"map": figure, "county": county}