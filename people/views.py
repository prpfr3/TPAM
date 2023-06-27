import json
import urllib

import wikipediaapi
from django.forms.models import model_to_dict
from django.db.models import Q
from django.shortcuts import render

from locos.models import LocoClass

from mainmenu.views import pagination

from .forms import *
from .models import *


def index(request):
    return render(request, "people/index.html")


def people(request):
    errors = None
    page = None

    if request.method == "POST":
        selection_criteria = PersonSelectionForm(request.POST)

        if (
            selection_criteria.is_valid()
            and selection_criteria.cleaned_data is not None
        ):
            conditions = Q()
            cleandata = selection_criteria.cleaned_data

            if "name" in cleandata and cleandata["name"]:
                conditions &= Q(name__icontains=cleandata["name"])

            if "role" in cleandata and cleandata["role"]:
                fk = cleandata["role"].id  # Store the role ID
                conditions &= Q(personrole__role_id=fk)

            if "source" in cleandata and cleandata["source"]:
                conditions &= Q(source=cleandata["source"])

            if "birthyear" in cleandata and cleandata["birthyear"]:
                conditions &= Q(birthdate__startswith=cleandata["birthyear"])

            if "diedyear" in cleandata and cleandata["diedyear"]:
                conditions &= Q(dieddate__startswith=cleandata["diedyear"])

            queryset = (
                Person.objects.filter(conditions)
                .prefetch_related("references")
                .order_by("surname", "firstname")
            )

            # Save the selection criteria values in the session
            request.session["name"] = cleandata.get("name")
            request.session["role_id"] = (
                cleandata.get("role").id if cleandata.get("role") else None
            )
            request.session["source"] = cleandata.get("source")
            request.session["birthyear"] = cleandata.get("birthyear")
            request.session["diedyear"] = cleandata.get("diedyear")
        else:
            errors = selection_criteria.errors
            queryset = Person.objects.prefetch_related("references").order_by(
                "surname", "firstname"
            )

    else:
        previous_criteria = {
            "name": request.session.get("name"),
            "role_id": request.session.get("role_id"),
            "source": request.session.get("source"),
            "birthyear": request.session.get("birthyear"),
            "diedyear": request.session.get("diedyear"),
        }

        if previous_criteria["role_id"]:
            previous_criteria["role"] = Role.objects.get(
                id=previous_criteria["role_id"]
            )
        else:
            previous_criteria["role"] = None

        selection_criteria = PersonSelectionForm(
            initial=previous_criteria, clear_previous_criteria=True
        )
        queryset = Person.objects.prefetch_related("references").order_by(
            "surname", "firstname"
        )

    queryset, page = pagination(
        request, queryset
    )  # Pass the updated queryset to the pagination function

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "page": page,
        "people": queryset,
    }

    return render(request, "people/people.html", context)


def person(request, person_id):
    person = Person.objects.get(id=person_id)
    references = Reference.objects.filter(person=person_id)
    designed_loco_classes = LocoClass.objects.filter(designer_person=person_id)

    # Get text describing the person either from a notes app research article, else Wikipedia, else none
    if person.post_fk:
        description = person.post_fk.body
        description_type = "Notes"
    elif person.wikitextslug:
        wiki_wiki = wikipediaapi.Wikipedia(
            language="en", extract_format=wikipediaapi.ExtractFormat.HTML
        )
        slug = urllib.parse.unquote(
            person.wikitextslug, encoding="utf-8", errors="replace"
        )
        description = wiki_wiki.page(slug).text
        description_type = "From Wikipedia:-"
    else:
        description = None
        description_type = None

    context = {
        "person": person,
        "references": references,
        "designed_loco_classes": designed_loco_classes,
        "description_type": description_type,
        "description": description,
    }
    return render(request, "people/person.html", context)


def people_timeline(request):
    import markdown

    people = Person.objects.filter(personrole__role_id=167).order_by("name")

    tdict = {
        "title": {
            "media": {"url": "", "caption": "", "credit": ""},
            "text": {
                "headline": "LSWR Chief Mechanical Engineers Timeline",
                "text": "<p>Timeline and the Wikipedia entries for Chief Mechanical Engineers / Locomotive Superintendents of the London and South Western Railway</p>",
            },
        },
        "events": [],
    }

    forlooplimiter = 0

    for person in people:
        if forlooplimiter < 20 and person.birthdate and person.dieddate:
            forlooplimiter += 1

            event = {
                "media": {
                    "url": person.wikiimageslug,
                    "caption": person.wikiimagetext,
                    "credit": "Caption Credit: All credit to Wikipedia",
                },
                "start_date": {"year": person.birthdate[:4]},
                "end_date": {"year": person.dieddate[:4]},
                "text": {"headline": person.name, "text": ""},
            }

            html_string = markdown.markdown(
                f"https://en.wikipedia.org/wiki/{person.wikitextslug}"
            )
            event["text"]["text"] = html_string.replace('"', "'")

            pagename = person.wikitextslug.replace("_", " ")
            wiki_wiki = wikipediaapi.Wikipedia(
                language="en", extract_format=wikipediaapi.ExtractFormat.HTML
            )

            if person.wikitextslug and wiki_wiki.page(person.wikitextslug).exists:
                text_array = wiki_wiki.page(person.wikitextslug).text.split(
                    "<h2>References</h2>"
                )
                event["text"] = {"text": text_array[0], "headline": pagename}
            else:
                event["text"] = {"text": html_string, "headline": pagename}

            tdict["events"].append(event)

    timeline_json = json.dumps(tdict)
    return render(
        request, "people/people_timeline.html", {"timeline_json": timeline_json}
    )


def people_vis_timeline(request):
    people = Person.objects.order_by("name")
    events = []
    forlooplimiter = 0

    for person in people:
        if person.birthdate and person.dieddate:
            forlooplimiter += 1
            # For format see https://visjs.github.io/vis-timeline/docs/timeline/#Data_Format
            event = {
                "id": forlooplimiter,
                "content": person.name,
                # Replace any unknown part of the date with 01 as vis_timeline requires full date
                "start": person.birthdate.replace("??", "01"),
                "end": person.dieddate.replace("??", "01"),
                "event.type": "point",
            }
            events.append(event)

    return render(
        request,
        "people/people_vis_timeline.html",
        {"timeline_json": json.dumps(events)},
    )
