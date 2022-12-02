import datetime
import json
from itertools import chain

import wikipediaapi
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, ExpressionWrapper, F, fields
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *

def pagination(request, queryset):
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

    return(queryset, page)

def index(request):
  return render(request, 'locos/index.html')


def builder(request, builder_id):
  builder = Builder.objects.get(id=builder_id)
  context = {'builder': builder}
  return render(request, 'locos/manufacturer.html', context)

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

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'builder_list': queryset, 'page': page}
    return render(request, 'locos/builder_list.html', context)


def company(request, company_id):
  company = Company.objects.get(id=company_id)
  wiki_categories = CompanyCategory.objects.filter(company=company_id)
  context = {'company': company, 'wiki_categories': wiki_categories}
  return render(request, 'locos/company.html', context)

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

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'company_list': queryset, 'page': page}
    return render(request, 'locos/company_list.html', context)


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

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'person_list': queryset, 'page': page}
    return render(request, 'locos/person_list.html', context)

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
      ## For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
      event = {"id": forlooplimiter,
              "content": person.name,
              "start": person.birthdate.replace("??", "01"), #Replace any unknown part of the date with 01 as vis_timeline requires full date
              "end": person.dieddate.replace("??", "01"),
              "event.type": 'point'}
      events.append(event)

  return render(request, 'locos/persons_vis_timeline.html', {'timeline_json':json.dumps(events)})

def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  context = {'loco_class': loco_class}
  return render(request, 'locos/loco_class.html', context)

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

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'page': page, 'loco_class_list': queryset}
    return render(request, 'locos/loco_class_list.html', context)

def loco_class(request, loco_class_id):
  loco_class = LocoClass.objects.get(id=loco_class_id)
  locomotives = Locomotive.objects.filter(lococlass=loco_class_id)
  references = Reference.objects.filter(lococlass=loco_class_id)
  images = Reference.objects.filter(type='6').order_by('citation')
  operators = loco_class.company_owneroperator.all()
  class_designers1 = loco_class.person_designer.all()
  class_designers2 = loco_class.builder_designer.all()  
  class_designers3 = loco_class.company_designer.all()
  class_designers = list(chain(class_designers1, class_designers2, class_designers3))
  class_builders1 = loco_class.person_builder.all()
  class_builders2 = loco_class.builder_builder.all()
  class_builders3 = loco_class.company_builder.all()
  class_builders = list(chain(class_builders1, class_builders2, class_builders3))

  wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
  page_name = loco_class.wikiname.replace(' ', '_')
  wikipedia_summary = wiki_wiki.page(page_name).text

  context = {'loco_class':loco_class,
              'locomotives':locomotives,
              'operators':operators,
              'references':references,
              'images':images,
              'designers':class_designers,
              'builders':class_builders,
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
            age = ExpressionWrapper(F('withdrawn_datetime')-F('build_datetime'), \
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
            queryset = Locomotive.objects.order_by('identifier')
    else:
        selection_criteria = LocomotiveSelectionForm()
        errors = selection_criteria.errors or None
        queryset = Locomotive.objects.order_by('identifier')

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'page': page, 'locomotives_list': queryset}
    return render(request, 'locos/locomotives_list.html', context)

def locomotive(request, locomotive_id):
    locomotive = Locomotive.objects.get(id=locomotive_id)
    try:
        lococlass = LocoClass.objects.get(id=locomotive.lococlass)
    except ObjectDoesNotExist:
        lococlass = None
        operators = None
        class_designers = None
        class_designers2 = None
        class_designers3 = None
        class_builders = None
        class_builders2 = None
        class_builders3 = None
    except Exception as e:
        print(f'{e=}')
    else:
      operators = lococlass.company_owneroperator.all()
      class_designers1 = lococlass.location_event_designer.all()
      class_designers2 = lococlass.builder_designer.all()
      class_designers3 = lococlass.company_designer.all()

      class_designers = list(chain(class_designers1, class_designers2, class_designers3))

      class_builders1 = lococlass.location_event_builder.all()
      class_builders2 = lococlass.builder_builder.all()
      class_builders3 = lococlass.company_builder.all()

      class_builders = list(chain(class_builders1, class_builders2, class_builders3))

    references = LocoClassSighting.objects.filter(loco=locomotive_id)
    images = Reference.objects.filter(loco=locomotive_id)

    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    # The following could be introduced at a later date for where there is a Wikipedia page for a locomotive
    # page_name = locomotive.wikipedia_name.replace(' ', '_') 
    # wikipedia_summary = wiki_wiki.page(page_name).text

    context = {'locomotive':locomotive,
                'lococlass':lococlass,
                'operators':operators,
                'references':references,
                'images':images,
                'designers':class_designers,
                'builders':class_builders,
                # 'wikipedia_summary':wikipedia_summary,
    }

    return render(request, 'locos/locomotive.html', context)