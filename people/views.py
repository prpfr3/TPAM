import json
import urllib
import markdown
import wikipediaapi
from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import QueryDict

from locos.models import LocoClass
from mainmenu.views import pagination
from .forms import *
from .models import *


def index(request):
    return render(request, "people/index.html")


def people(request):
    errors = None

    # Check if the queryset is already cached and, if not, retrieve and cache it
    queryset = cache.get("cached_queryset")
    if queryset is None:
        queryset = Person.objects.prefetch_related("references").order_by(
            "surname", "firstname"
        )
        cache.set("cached_queryset", queryset, timeout=None)  # Cache it

    # Load selection criteria from session if available, or use empty data on first load
    if request.method == "POST":
        selection_criteria = PersonSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["person_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("person_selection_criteria", None)
        selection_criteria = PersonSelectionForm(form_data)

    # Default queryset for all persons
    if selection_criteria.is_valid():
        # Build the queryset based on valid selection criteria
        queryset = people_query_build(selection_criteria.cleaned_data)
    else:
        errors = selection_criteria.errors

    queryset = pagination(request, queryset, 8)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "people/people.html", context)


def people_query_build(selection_criteria):
    conditions = Q()
    cleandata = selection_criteria

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

    # Cache it indefinitely
    cache.set("cached_queryset", queryset, timeout=None)
    return queryset


def person(request, slug):
    person = Person.objects.get(slug=slug)
    references = Reference.objects.filter(person=person.id)
    designed_loco_classes = LocoClass.objects.filter(designer_person=person.id)

    # Get text describing the person either from a notes app research article, else Wikipedia, else none
    if person.posts.exists():
        first_post = person.posts.first()  # Get the first post in the queryset
        description_type = first_post.title
        description = first_post.body
    elif person.wikitextslug:
        wiki_wiki = wikipediaapi.Wikipedia(
            language="en",
            user_agent="github/prpfr3 TPAM",
            extract_format=wikipediaapi.ExtractFormat.HTML,
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


def people_spreadsheet(request):
    people = Person.objects.all()
    return render(request, "people/people_spreadsheet.html", {"people": people})


def people_storyline(request):
    errors = None
    page = None

    if request.method == "POST":
        selection_criteria = PersonTimelineSelectionForm(request.POST)

        if (
            selection_criteria.is_valid()
            and selection_criteria.cleaned_data is not None
        ):
            timeline_json = people_storyline_build(selection_criteria, request)
            return render(
                request,
                "people/people_storyline.html",
                {"timeline_json": timeline_json},
            )
        else:
            errors = selection_criteria.errors
            queryset = Person.objects.prefetch_related("references").order_by(
                "surname", "firstname"
            )

    else:
        previous_criteria = {
            "role_id": request.session.get("role_id"),
            "birthyear": request.session.get("birthyear"),
            "diedyear": request.session.get("diedyear"),
        }

        if previous_criteria["role_id"]:
            previous_criteria["role"] = Role.objects.get(
                id=previous_criteria["role_id"]
            )
        else:
            previous_criteria["role"] = None

        selection_criteria = PersonTimelineSelectionForm(
            initial=previous_criteria, clear_previous_criteria=True
        )
        queryset = Person.objects.prefetch_related("references").order_by(
            "surname", "firstname"
        )

    queryset = pagination(request, queryset)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "people": queryset,
    }

    return render(request, "people/people_storyline_selection.html", context)


def people_storyline_build(selection_criteria, request):
    conditions = Q()
    header = ""
    cleandata = selection_criteria.cleaned_data

    if "name" in cleandata and cleandata["name"]:
        conditions &= Q(name__icontains=cleandata["name"])

    if "role" in cleandata and cleandata["role"]:
        fk = cleandata["role"].id  # Store the role ID
        conditions &= Q(personrole__role_id=fk)
        header += str(cleandata["role"])

    if "birthyear" in cleandata and cleandata["birthyear"]:
        conditions &= Q(birthdate__startswith=cleandata["birthyear"])
        header += "Born In " + str(cleandata["birthyear"])

    if "diedyear" in cleandata and cleandata["diedyear"]:
        conditions &= Q(dieddate__startswith=cleandata["diedyear"])
        header += "Died In " + str(cleandata["diedyear"])

    people = (
        Person.objects.filter(conditions)
        .prefetch_related("references")
        .annotate(
            date_from=F("personrole__date_from"), date_to=F("personrole__date_to")
        )
        .order_by("surname", "firstname")
    )

    tdict = {
        "title": {
            "media": {"url": "", "caption": "", "credit": ""},
            "text": {
                "headline": "Biographies",
                "text": header,
            },
        },
        "events": [],
    }

    forlooplimiter = 0

    for person in people:
        if (person.date_from and person.date_to) or (
            person.birthdate and person.dieddate
        ):

            if (
                person.date_from and person.date_to
            ):  # i.e. the date range should be for the role rather than born/died
                start_date = person.date_from[:4]
                end_date = person.date_to[:4]
            else:
                start_date = person.birthdate[:4]
                end_date = person.dieddate[:4]

            event = {
                "media": {
                    "url": person.wikiimageslug,
                    "caption": person.wikiimagetext,
                    "credit": "Caption Credit: All credit to Wikipedia",
                },
                "start_date": {"year": start_date},
                "end_date": {"year": end_date},
                "text": {"headline": person.name, "text": ""},
            }

            html_string = markdown.markdown(
                f"https://en.wikipedia.org/wiki/{person.wikitextslug}"
            )
            event["text"]["text"] = html_string.replace('"', "'")

            pagename = person.wikitextslug.replace("_", " ")
            wiki_wiki = wikipediaapi.Wikipedia(
                language="en",
                user_agent="github/prpfr3 TPAM",
                extract_format=wikipediaapi.ExtractFormat.HTML,
            )

            if person.wikitextslug and wiki_wiki.page(person.wikitextslug).exists:
                text_array = wiki_wiki.page(person.wikitextslug).text.split(
                    "<h2>References</h2>"
                )
                event["text"] = {"text": text_array[0], "headline": pagename}
            else:
                event["text"] = {"text": html_string, "headline": pagename}

            tdict["events"].append(event)

        with open("CMEs.json", "w") as output_file:
            json.dump(tdict, output_file, indent=4)

    return json.dumps(tdict)


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
