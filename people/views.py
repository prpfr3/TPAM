import json

from django.shortcuts import render

from mainmenu.views import pagination

from .forms import *
from .models import *

def index(request):
  return render(request, 'people/index.html')

def people(request):
    
    errors = None
    from pprint import pprint
    if request.method == 'POST':
        selection_criteria = PersonSelectionForm(request.POST)
        if not selection_criteria.is_valid():
            errors = selection_criteria.errors
            queryset = Person.objects.order_by('name')
            print('0:-', queryset)
        elif str(selection_criteria.cleaned_data['name']):
            queryset = Person.objects.filter(name__icontains=selection_criteria.cleaned_data['name']).order_by('name')
            print('1:-', queryset)
        elif len(selection_criteria.cleaned_data['role']) != 0:
            
            queryset = Person.objects.filter(role__in=selection_criteria.cleaned_data['role']).order_by('name')
            print('2:-', selection_criteria.cleaned_data['role'], queryset)
 
        elif str(selection_criteria.cleaned_data['source']) != 'None':
            queryset = Person.objects.filter(source=selection_criteria.cleaned_data['source']).order_by('name')
            print('3:-', queryset)
    else:
        selection_criteria = PersonSelectionForm()
        errors = selection_criteria.errors
        queryset = Person.objects.order_by('name')
        print('4:-', queryset)

    queryset, page = pagination(request, queryset)

    context = {'selection_criteria':selection_criteria, 'errors': errors, 'people': queryset, 'page': page}
    
    pprint(context)
    return render(request, 'people/people.html', context)

def people_timeline(request):
  people = Person.objects.order_by('name')

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

  for person in people:

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
            "text": ""
          }
        }

      tdict['events'].append(event)

  timeline_json = json.dumps(tdict)
  return render(request, 'people/people_timeline.html', {'timeline_json':timeline_json})

def people_vis_timeline(request):
  people = Person.objects.order_by('name')
  events = []
  forlooplimiter = 0

  for person in people:
    if person.birthdate and person.dieddate:
      forlooplimiter += 1
      ## For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
      event = {"id": forlooplimiter,
              "content": person.name,
              "start": person.birthdate.replace("??", "01"), #Replace any unknown part of the date with 01 as vis_timeline requires full date
              "end": person.dieddate.replace("??", "01"),
              "event.type": 'point'}
      events.append(event)

  return render(request, 'people/people_vis_timeline.html', {'timeline_json':json.dumps(events)})