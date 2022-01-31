from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import LocoClassSighting, ClassBuilder, Person, Image, ModernClass, LocoClass, Builder, Company, Sighting, CompanyCategory, ClassDesigner
from .forms import PersonForm, ImageForm
import json
import pprint

def index(request):
  return render(request, 'locos/index.html')

def persons(request):
  persons = Person.objects.order_by('name')
  
  # This serializer needs further work. See bookr for a possible model
  # persons_with_roles = []
  # for person in persons:
  #   personroles = person.personrole_set.all()
  #   for personrole in personroles:
  #     persons_with_roles.append({"person": person})
  # context = {'persons': persons_with_roles}

  context = {'persons': persons}
  return render(request, 'locos/person_list.html', context)

def sightings_storymap(request):
  sightings = Sighting.objects.order_by('id')
  
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

  for sighting in sightings:

    if forlooplimiter < 13:
      forlooplimiter += 1

      slide_date = str(sighting.DD) + "/" + str(sighting.MM) + "/" + str(sighting.YD) + str(sighting.YY)
      slide_media_caption = str(sighting.location_description) + " on " + str(sighting.DD) + "/" + str(sighting.MM) + "/" + str(sighting.YD) + str(sighting.YY)
      slide_media_credit = sighting.citation + ' ' + sighting.citation_specifics
      slide_headline = str(sighting.location_description) + " on " + str(sighting.DD) + "/" + str(sighting.MM) + "/" + str(sighting.YD) + str(sighting.YY)

      slide = { 
        "background": {"url": ""}, 
        "date": slide_date, 
        "location": {"lat": sighting.northing, "line": True, "lon": sighting.easting, "zoom": 12}, 
        "media": {"caption": slide_media_caption, "credit": slide_media_credit, "url": sighting.hyperlink}, 
        "text": {"headline": slide_headline, "text": sighting.notes}
      }

      storymap_dict['storymap']['slides'].append(slide)

  storymap_json = json.dumps(storymap_dict)
  return render(request, 'locos/sightings_storymap.html', {'storymap_json':storymap_json})

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

def person(request, person_id):
  person = Person.objects.get(id=person_id)
  context = {'person': person}
  return render(request, 'locos/person.html', context)

@login_required
def new_person(request):
  if request.method != 'POST':
    form = PersonForm()
  else:
    form = PersonForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:persons'))

  context = {'form': form}
  return render(request, 'locos/person_new.html', context)

@login_required
def edit_person(request, person_id):
  person = Person.objects.get(id=person_id)

  if request.method != 'POST':
    form = PersonForm(instance=person)
  else:
    form = PersonForm(instance=person, data=request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('locos:person', args=[person_id]))

  context = {'person': person,'form': form}
  return render(request, 'locos/person_edit.html', context)

def loco_classes(request):
  loco_classes = LocoClass.objects.order_by('grouping_company', 'pre_grouping_company', 'grouping_class')
  context = {'loco_classes': loco_classes}
  return render(request, 'locos/loco_class_list.html', context)

def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  operators = Company.objects.filter(loco_classes=loco_class_id)
  sightings = Sighting.objects.filter(lococlass=loco_class_id)
  class_designers1 = loco_class.person_designer.all()
  class_designers2 = loco_class.builder_designer.all()
  class_designers3 = loco_class.company_designer.all()
  class_builders1 = loco_class.person_builder.all()
  class_builders2 = loco_class.builder_builder.all()
  class_builders3 = loco_class.company_builder.all()

  context = {'loco_class':loco_class, 
              'operators':operators, 
              'sightings':sightings, 
              'designers1':class_designers1, 
              'designers2':class_designers2,
              'designers3':class_designers3,
              'builders1':class_builders1, 
              'builders2':class_builders2,
              'builders3':class_builders3}
  return render(request, 'locos/loco_class.html', context)


def companies(request):
  companies = Company.objects.order_by('name')
  context = {'companies': companies}
  return render(request, 'locos/company_list.html', context)

def company(request, company_id):
  company = Company.objects.get(id=company_id)
  wiki_categories = CompanyCategory.objects.filter(company=company_id)
  context = {'company': company, 'wiki_categories': wiki_categories}
  return render(request, 'locos/company.html', context)

def builders(request):
  builder = Builder.objects.order_by('name')
  context = {'builder': builder}
  return render(request, 'locos/manufacturer_list.html', context)

def builder(request, builder_id):
  builder = Builder.objects.get(id=builder_id)
  context = {'builder': builder}
  return render(request, 'locos/manufacturer.html', context)

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