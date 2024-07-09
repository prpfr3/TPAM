# from django.shortcuts import render
# from .forms import *


# def regional_map_select(request):
#     if request.method == "POST":
#         region_form = RegionChoiceForm(request.POST)

#         if region_form.is_valid():
#             return region_form.cleaned_data["regions"]
#     else:
#         region_form = RegionChoiceForm()

#     context = {
#         "region_form": region_form,
#     }
#     return render(request, "locations/region_select.html", context)
