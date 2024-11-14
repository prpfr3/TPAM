from itertools import chain

import wikipediaapi
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from notes.models import Reference
from mainmenu.views import pagination
from .forms import *
from .models import *


def index(request):
    return render(request, "locos/index.html")


def loco_classes(request):
    errors = None
    items_per_page = 30

    # Load selection criteria from session if available, or use empty data on first load
    if request.method == "POST":
        selection_criteria = LocoClassSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["loco_class_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("loco_class_selection_criteria", None)
        selection_criteria = LocoClassSelectionForm(form_data)

    # Default queryset for all loco classes
    queryset = LocoClass.objects.order_by("name")

    if selection_criteria.is_valid():
        # Build the queryset based on valid selection criteria
        queryset = loco_classes_query_build(selection_criteria.cleaned_data)
    else:
        errors = selection_criteria.errors

    queryset = pagination(request, queryset, items_per_page)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "locos/motive_power_classes.html", context)


def loco_classes_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "name" in cleandata and cleandata["name"]:
        conditions &= Q(name__icontains=cleandata["name"])

    if "wheel_body_type" in cleandata and cleandata["wheel_body_type"]:
        conditions &= Q(wheel_body_type__icontains=cleandata["wheel_body_type"])

    if "wheel_arrangement" in cleandata and cleandata["wheel_arrangement"]:
        fk = cleandata["wheel_arrangement"]
        conditions &= Q(wheel_arrangement_id=fk)

    if "designer_person" in cleandata and cleandata["designer_person"]:
        fk = cleandata["designer_person"]
        conditions &= Q(designer_person_id=fk)

    if "owner_operators" in cleandata and cleandata["owner_operators"]:
        fk = cleandata["owner_operators"]
        conditions &= Q(owner_operators=fk)

    if "manufacturers" in cleandata and cleandata["manufacturers"]:
        fk = cleandata["manufacturers"]
        conditions &= Q(manufacturers=fk)

    if "power_type" in cleandata and cleandata["power_type"]:
        conditions &= Q(power_type__icontains=cleandata["power_type"])

    queryset = LocoClass.objects.filter(conditions).order_by("name")
    # .annotate(total=Count("brd_class_name"))

    return queryset


def loco_class(request, slug):

    loco_class = LocoClass.objects.filter(slug=slug).order_by("name").first()

    locomotives = Locomotive.objects.filter(lococlass=loco_class.id).order_by(
        "number_as_built"
    )

    references = loco_class.references.all()
    operators = loco_class.owner_operators.all()
    manufacturers = loco_class.manufacturers.all()
    posts = loco_class.posts.all()

    context = {
        "loco_class": loco_class,
        "posts": posts,
        "locomotives": locomotives,
        "operators": operators,
        "references": references,
        "manufacturers": manufacturers,
    }

    return render(request, "locos/motive_power_class.html", context)


@login_required
def locomotives(request):
    errors = None
    # Default queryset for all locomotives
    queryset = Locomotive.objects.order_by("name")

    # Load selection criteria from session if available, or use empty data on first load
    if request.method == "POST":
        selection_criteria = LocomotiveSelectionForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["locomotive_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("locomotive_selection_criteria", None)
        selection_criteria = LocomotiveSelectionForm(form_data)

    # Filter based on selection criteria
    if (
        selection_criteria.is_valid()
        and selection_criteria.cleaned_data["number_as_built"]
    ):
        queryset = Locomotive.objects.filter(
            number_as_built__icontains=selection_criteria.cleaned_data.get(
                "number_as_built", ""
            )
        )

    queryset = pagination(request, queryset)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }
    return render(request, "locos/motive_power_list.html", context)


@login_required
def locomotive(request, locomotive_id):
    lococlass = None
    operators = None
    class_designers = None
    class_designers2 = None
    class_designers3 = None
    class_manufacturers = None
    class_manufacturers2 = None
    class_manufacturers3 = None
    locomotive = Locomotive.objects.get(id=locomotive_id)
    try:
        lococlass = LocoClass.objects.get(id=locomotive.lococlass)
    except ObjectDoesNotExist:
        pass
    except Exception as e:
        print(f"{e=}")
    else:
        operators = lococlass.company_owneroperator.all()
        class_designers1 = lococlass.location_event_designer.all()
        class_designers2 = lococlass.manufacturer_designer.all()
        class_designers3 = lococlass.company_designer.all()

        class_designers = list(
            chain(class_designers1, class_designers2, class_designers3)
        )

        class_manufacturers1 = lococlass.location_event_manufacturer.all()
        class_manufacturers2 = lococlass.manufacturer_manufacturer.all()
        class_manufacturers3 = lococlass.company_manufacturer.all()

        class_manufacturers = list(
            chain(class_manufacturers1, class_manufacturers2, class_manufacturers3)
        )

    # references = Reference.objects.filter(loco=locomotive_id)

    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent="github/prpfr3 TPAM",
        language="en",
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    # The following could be introduced at a later date for where there is a Wikipedia page for a locomotive
    # page_name = locomotive.wikipedia_name.replace(' ', '_')
    # wikipedia_summary = wiki_wiki.page(page_name).text

    context = {
        "locomotive": locomotive,
        "lococlass": lococlass,
        "operators": operators,
        # 'references':references,
        "designers": class_designers,
        "manufacturers": class_manufacturers,
        # 'wikipedia_summary':wikipedia_summary,
    }

    return render(request, "locos/motive_power.html", context)


def photos(request):
    # Photos are currently not catalogued with information
    # The LocomotiveImageForm is therefore not displayed and this
    # view will display all records.
    errors = None
    queryset = Image.objects.all()

    # Load selection criteria from session if available
    if request.method == "POST":
        selection_criteria = LocomotiveImageForm(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["photo_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("photo_selection_criteria", None)
        selection_criteria = LocomotiveImageForm(form_data)

    # Filter queryset based on selection criteria
    if selection_criteria.is_valid():
        # queryset = Image.objects.all()
        queryset = photos_query_build(selection_criteria.cleaned_data)

    queryset = pagination(request, queryset, 27)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "locos/photos.html", context)


def photos_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "image_name" in cleandata and cleandata["image_name"]:
        conditions &= Q(image_name__icontains=cleandata["image_name"])

    if "heritage_site" in cleandata and cleandata["heritage_site"]:
        fk = cleandata["heritage_site"]
        conditions &= Q(location=fk)

    queryset = Image.objects.filter(conditions).order_by("image_name")
    return queryset


def photo(request, photo_id):
    photo = Image.objects.get(id=photo_id)
    context = {"photo": photo}
    return render(request, "locos/photo.html", context)
