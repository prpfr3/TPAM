from django.db.models import Q
from django.shortcuts import render, redirect
from mainmenu.views import pagination
from .forms import *
from .models import *


def brmplans(request):

    errors = None
    queryset = BRMPlans.objects.all()

    # Load selection criteria from session if available
    if request.method == "POST":
        selection_criteria = BRMPlansSelect(request.POST)
        if selection_criteria.is_valid():
            # Save criteria to session
            request.session["brmplans_selection_criteria"] = request.POST.dict()
            return redirect(request.path_info)
    else:
        # Initialize form with session-stored data or empty if none available
        form_data = request.session.get("brmplans_selection_criteria", None)
        selection_criteria = BRMPlansSelect(form_data)

    # Filter queryset based on selection criteria
    if selection_criteria.is_valid():
        # queryset = Image.objects.all()
        queryset = brmplans_query_build(selection_criteria.cleaned_data)

    queryset = pagination(request, queryset, 27)

    context = {
        "selection_criteria": selection_criteria,
        "errors": errors,
        "queryset": queryset,
    }

    return render(request, "brmsra/brmplans.html", context)


def brmplans_query_build(selection_criteria):

    conditions = Q()
    cleandata = selection_criteria

    if "archivenumber" in cleandata and cleandata["archivenumber"]:
        conditions &= Q(archivenumber__icontains=cleandata["archivenumber"])

    if "location" in cleandata and cleandata["location"]:
        conditions &= Q(location__icontains=cleandata["location"])

    if "description" in cleandata and cleandata["description"]:
        conditions &= Q(description__icontains=cleandata["description"])

    queryset = BRMPlans.objects.filter(conditions).order_by("archivenumber")
    return queryset


def brmplan(request, plan_id):
    plan = BRMPlans.objects.get(id=plan_id)
    context = {"plan": plan}
    return render(request, "brmsra/brmplan.html", context)
 
