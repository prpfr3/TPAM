# import folium
# from folium.plugins import MarkerCluster

# from django.db import connection
# from django.http import JsonResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
# from django.views.generic import TemplateView
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import D
# from django.db.models import Q


# from .forms import *
# from .models import *
# from mainmenu.models import Profile

# # from shapely.geometry import Point
# from geopy.geocoders import Nominatim


# def index(request):
#     return render(request, "ukheritage\index.html")


# def execute_sql(sql, parameters):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql, parameters)
#             result = cursor.fetchall()

#     except Exception as e:
#         print(e)

#     return result


# def map_points(results, marker_cluster, basemap, markers_only=False):
#     for point in results:
#         label_string = f'<a href="{point[1]} "target="_blank">{point[0]}</a>'
#         label_html = folium.Html(label_string, script=True)
#         label = folium.Popup(label_html, max_width=2650)
#         folium.Marker(
#             location=(point[2], point[3]), popup=label, tooltip=str(point[0])
#         ).add_to(marker_cluster)
#         if not markers_only:
#             folium.GeoJson(data=point[4]).add_to(basemap)


# class HeritageMap(TemplateView):

#     template_name = "ukheritage/heritage_map.html"

#     def get_context_data(self, **kwargs):
#         geo_area = self.kwargs["geo_area"]

#         sql = """SELECT ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry)) FROM public."locations_UK_admin_boundaries" WHERE ctyua19nm = %s;"""
#         sql = """SELECT ST_Y(ST_CENTROID(geometry)), ST_X(ST_CENTROID(geometry)) FROM public."locations_ukarea" WHERE "ITL121NM" = %s;"""
#         centroid = execute_sql(sql, [geo_area])

#         basemap = folium.Map(
#             centroid[0],
#             zoom_start=10,
#             tiles="cartodb positron",
#             prefer_canvas=True,
#             height=500,
#         )
#         marker_cluster = MarkerCluster().add_to(basemap)

#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_parks_gardens" as a JOIN public."locations_UK_admin_boundaries" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b.ctyua19nm = %s ;
#         """
#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_parks_gardens" as a JOIN public."locations_ukarea" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b."ITL121NM" = %s ;
#         """
#         results = execute_sql(sql, [geo_area])
#         map_points(results, marker_cluster, basemap)

#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_listed_buildings" as a JOIN public."locations_UK_admin_boundaries" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b.ctyua19nm = %s
#         AND
#         (a."Grade" = 'I' OR a."Grade" = 'II*');
#         """
#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_listed_buildings" as a JOIN public."locations_ukarea" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b."ITL121NM" = %s
#         AND
#         (a."Grade" = 'I' OR a."Grade" = 'II*');
#         """
#         results = execute_sql(sql, [geo_area])
#         map_points(results, marker_cluster, basemap, markers_only=True)

#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_scheduled_monuments" as a JOIN public."locations_UK_admin_boundaries" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b.ctyua19nm = %s;
#         """
#         sql = """
#         SELECT a."Name", a."Hyperlink", ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_scheduled_monuments" as a JOIN public."locations_ukarea" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b."ITL121NM" = %s;
#         """
#         results = execute_sql(sql, [geo_area])
#         map_points(results, marker_cluster, basemap, markers_only=True)

#         sql = """
#         SELECT a."Name", '' AS Hyperlink, ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_always_open_land" as a JOIN public."locations_UK_admin_boundaries" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b.ctyua19nm = %s;
#         """
#         sql = """
#         SELECT a."Name", '' AS Hyperlink, ST_Y(ST_CENTROID(a.geometry)), ST_X(ST_CENTROID(a.geometry)), ST_AsGeoJSON(a.geometry)
#         FROM
#         public."gd_UK_always_open_land" as a JOIN public."locations_ukarea" as b
#         ON ST_WITHIN(a.geometry, b.geometry)
#         WHERE b."ITL121NM" = %s;
#         """
#         results = execute_sql(sql, [geo_area])
#         map_points(results, marker_cluster, basemap)

#         figure = folium.Figure()
#         basemap.add_to(figure)
#         figure.render()
#         return {"map": figure, "title": geo_area}


# def county_select(request):
#     if request.method == "POST":
#         counties = CountySelectForm(request.POST)

#         if counties.is_valid():
#             selected_county = counties.cleaned_data["counties"]
#             geo_area = str(selected_county)
#             return HttpResponseRedirect(
#                 reverse("ukheritage:heritage_map", args=[geo_area])
#             )
#     else:
#         counties = CountySelectForm()
#         errors = counties.errors or None
#         context = {
#             "counties": counties,
#             "errors": errors,
#         }
#         return render(request, "ukheritage/county_select.html", context)


# from locations.utils import RegionSelectView


# class RegionalMapSelectView(RegionSelectView):
#     redirect_view_name = "ukheritage:heritage_map"


# def listed_buildings_select(request):
#     if request.method != "POST":
#         sc = ListedBuildingsSelectionForm()
#     else:
#         sc = ListedBuildingsSelectionForm(request.POST)

#         if sc.is_valid() and sc.cleaned_data != None:
#             selected = sc.cleaned_data

#             if selected["location"] == False:
#                 selected["location"] = ""

#             Q1 = Q()
#             if selected["grades"] != None:
#                 for g in selected["grades"]:
#                     Q1 |= Q(grade=g)

#             Q2 = Q()

#             if selected["address"] != "":

#                 geocoder = Nominatim(#user_agent="github/prpfr3 TPAM")
#                 loc = geocoder.geocode(selected["address"])
#                 selected["longitude"] = loc.longitude
#                 selected["latitude"] = loc.latitude

#             if (
#                 selected["longitude"] == None
#                 and selected["latitude"] == None
#                 and selected["location"] != None
#             ):
#                 Q2 &= Q(location__icontains=selected["location"])
#             if selected["name"] != None:
#                 Q2 &= Q(name__icontains=selected["name"])

#             queryset2 = (
#                 GdUkListedBuildings.objects.filter(Q1, Q2)
#                 .select_related()
#                 .order_by("location", "grade", "name")
#             )

#             if len(queryset2) != 0:

#                 if selected["longitude"] != None and selected["latitude"] != None:
#                     origin_point = Point(
#                         selected["longitude"], selected["latitude"], srid=4326
#                     )
#                     folium_centroid = (selected["latitude"], selected["longitude"])
#                 else:
#                     coords = []
#                     for row in queryset2:
#                         coords_tuple = (row.geometry.y, row.geometry.x)
#                         coords.append(coords_tuple)

#                     x = [p[0] for p in coords]
#                     y = [p[1] for p in coords]
#                     xmean = sum(x) / len(coords)
#                     ymean = sum(y) / len(coords)
#                     folium_centroid = (xmean, ymean)
#                     origin_point = Point(ymean, xmean, srid=4277)

#                 queryset1 = queryset2.annotate(
#                     distance=Distance("geometry", origin_point)
#                 ).order_by("distance")
#                 queryset = queryset1.filter(
#                     distance__lte=D(km=selected["max_distance_kms"])
#                 )[0 : selected["max_items"]]

#                 if selected["map_or_list"] == "Map":

#                     figure = folium.Figure()
#                     m = folium.Map(
#                         folium_centroid,
#                         zoom_start=10,
#                         tiles="cartodbpositron",
#                         height=500,
#                         prefer_canvas=True,
#                     )
#                     m.add_to(figure)

#                     marker_cluster = MarkerCluster().add_to(m)

#                     for point in range(0, len(queryset)):

#                         href = (
#                             '<a href="'
#                             + str(queryset[point].hyperlink)
#                             + '"target="_blank">'
#                             + "Grade:"
#                             + str(queryset[point].grade)
#                             + " "
#                             + str(queryset[point].name)
#                             + "</a>"
#                         )

#                         label_html = folium.Html(href, script=True)
#                         label = folium.Popup(label_html, max_width=2650)
#                         coords_tuple = (
#                             queryset[point].geometry.y,
#                             queryset[point].geometry.x,
#                         )
#                         folium.Marker(
#                             location=coords_tuple,
#                             popup=label,
#                             tooltip=str(queryset[point].name),
#                         ).add_to(marker_cluster)

#                     figure.render()

#                     context = {"map": figure, "county": "Temporary"}
#                     return render(request, "ukheritage/heritage_map.html", context)

#                 elif selected["map_or_list"] == "List":

#                     context = {"sc": sc, "errors": sc.errors, "buildings": queryset}
#                     return render(
#                         request, "ukheritage/listed_buildings_select.html", context
#                     )

#     context = {"sc": sc, "errors": sc.errors or None, "buildings": None}
#     return render(request, "ukheritage/listed_buildings_select.html", context)


# def listed_buildings_nearby(request):
#     """
#     Pure Django and Django versions of this function are provided below. For the JS version:-
#     1. This function calls listed_buildings_nearby_js.html
#     2. listed_buildings_nearby_js.html calls listed_buildings.js
#     3. listed_buildings_js calls python django view function get_nearby_buildings
#     4. get_nearby_buildings function runs with each click and returns a JSONresponse to listed_buildings_js which populates elements of listed_buildings_nearby.html with the data
#     """

#     # Sets the location to Covent Garden as an example
#     longitude = -0.12317
#     latitude = 51.51133

#     """
#     # Query used for Pure Django solution
#     user_location = Point(longitude, latitude, srid=4326)
#     queryset = GdUkListedBuildings.objects.annotate(distance=Distance('geometry', user_location)).order_by('distance')[0:100]
#     """

#     form = ListedBuildingForm(request.POST or None)
#     # If statement executed if the user uses the JS modal to update the notes of an entry
#     if request.is_ajax() and form.is_valid():
#         instance = form.save(commit=False)
#         instance.author = Profile.objects.get(user=request.user)
#         instance.save()
#         return JsonResponse(
#             {
#                 "id": instance.id,
#                 "name": instance.name,
#                 "mynotes": instance.mynotes,
#             }
#         )

#     return render(request, "ukheritage/listed_buildings_nearby_js.html", {"form": form})

#     """
#     # Return for Pure Django solution
#     return render(request, "ukheritage/listed_buildings_nearby.html", {'queryset':queryset})
#     """


# def get_nearby_buildings(request, **kwargs):

#     if not request.is_ajax():
#         return

#     longitude = -0.12317
#     latitude = 51.51133
#     user_location = Point(longitude, latitude, srid=4326)
#     num_buildings = kwargs.get("num_buildings")

#     visible = 6
#     upper = num_buildings
#     lower = upper - visible
#     size = GdUkListedBuildings.objects.all().count()
#     queryset = GdUkListedBuildings.objects.annotate(
#         distance=Distance("geometry", user_location)
#     ).order_by("distance")[:100]

#     buildings = []
#     # New dictionary needed as distance cannot be serialized
#     for building in queryset:
#         item = {
#             "id": building.id,
#             "listed_building": building.name,
#             "distance": building.distance.m,
#             "liked": request.user in building.liked.all(),
#             "count": building.like_count,
#             "hyperlink": building.hyperlink,
#         }
#         buildings.append(item)

#     return JsonResponse({"buildings": buildings[lower:upper], "size": size})


# def building_detail(request, pk):
#     obj = GdUkListedBuildings.objects.get(id=pk)

#     if request.method != "POST":
#         form = ListedBuildingForm(instance=obj)
#     else:
#         form = ListedBuildingForm(instance=obj, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("ukheritage:listed_buildings_nearby"))

#     context = {"obj": obj, "form": form}
#     return render(request, "ukheritage/building_detail_js.html", context)


# def like_unlike_building(request):
#     if request.is_ajax():
#         pk = request.POST.get("pk")
#         building = GdUkListedBuildings.objects.get(pk=pk)
#         # If already 'liked; will need to unlike the post
#         if request.user in building.liked.all():
#             liked = False
#             building.liked.remove(request.user)
#         else:
#             liked = True
#             building.liked.add(request.user)
#         return JsonResponse({"liked": liked, "count": building.like_count})


# def myplaces(request):

#     # Sets the location to Covent Garden as an example
#     longitude = -0.12317
#     latitude = 51.51133

#     form = MyplacesForm(request.POST or None)
#     # If statement is executed when the user uses the JS modal to update the notes of an entry
#     if request.is_ajax() and form.is_valid():
#         instance = form.save(commit=False)
#         instance.author = Profile.objects.get(user=request.user)
#         instance.save()
#         return JsonResponse(
#             {
#                 "id": instance.id,
#                 "name": instance.name,
#                 "mynotes": instance.mynotes,
#             }
#         )

#     return render(request, "ukheritage/myplaces.html", {"form": form})


# def get_myplaces(request, **kwargs):

#     if not request.is_ajax():
#         return

#     longitude = -0.12317
#     latitude = 51.51133
#     user_location = Point(longitude, latitude, srid=4326)
#     num_places = kwargs.get("num_places")

#     visible = 6
#     upper = num_places
#     lower = upper - visible
#     size = MyPlaces.objects.all().count()
#     queryset = (
#         MyPlaces.objects.all()
#         .annotate(distance=Distance("geometry", user_location))
#         .order_by("distance")[:100]
#     )
#     places = []
#     for place in queryset:
#         distance = 0
#         if place.distance:
#             distance = place.distance.m
#         item = {
#             "id": place.id,
#             "name": place.name,
#             # 'distance': distance,
#             "favourite": request.user in place.favourite.all(),
#             "count": place.like_count,
#             "hyperlink": place.hyperlink,
#         }
#         places.append(item)
#     # places = serializers.serialize('json', queryset) #Would be simpler but does not work as cannot serialize the Distance field

#     return JsonResponse({"places": places[lower:upper], "size": size})


# def myplace(request, pk):
#     obj = MyPlaces.objects.get(id=pk)

#     if request.method != "POST":
#         form = MyplacesForm(instance=obj)
#         owner = obj.owner_id
#         user = request.user.id
#     else:
#         form = MyplacesForm(instance=obj, data=request.POST)
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(reverse("ukheritage:myplaces"))

#     data = {"obj": obj, "form": form, "author": owner, "logged_in": user}
#     return render(request, "ukheritage/myplace.html", data)


# def make_favourite(request):
#     if request.is_ajax():
#         pk = request.POST.get("pk")
#         place = MyPlaces.objects.get(pk=pk)
#         # If already a favourite will need to 'unfavourite' the place
#         if request.user in place.favourite.all():
#             favourite = False
#             place.favourite.remove(request.user)
#         else:
#             favourite = True
#             place.favourite.add(request.user)
#         return JsonResponse({"favourite": favourite, "count": place.like_count})
