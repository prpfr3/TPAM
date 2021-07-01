import os
import folium
import webbrowser


import pandas as pd
import geopandas as gpd
import altair as alt

from folium.plugins import MarkerCluster
from sqlalchemy import create_engine, text
from geopandas import GeoDataFrame
from shapely.geometry import Point
from vega_datasets import data
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm, TopicForm, EmailPostForm, LocationChoiceField

from .utils import get_plot, get_yahoo_shareprices, matplotlib_shareprices, mattest, bokeh_chart, shapefile_info

from .models import Shop, GdUkListedBuildings, GdUkAlwaysOpenLand, GdUkParksGardens, GdUkScheduledMonuments, UkAdminBoundaries, Topic, Post, HeritageSite, Visit

"""
# Some references for the ownerviews

 https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid

 https://stackoverflow.com/questions/862522/django-populate-user-id-when-saving-a-model

 https://stackoverflow.com/a/15540149

 https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview
"""

class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """

class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """

class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """

    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


def index(request):
  return render(request, 'maps/index.html')

def tube_map(request):
    return render(request, 'maps/tube_map.html')

def tube_map_chart(request):
    #This is called by 'maps/tube_map.html' to provide the chart

  boroughs = alt.topo_feature(data.londonBoroughs.url, 'boroughs')
  tubelines = alt.topo_feature(data.londonTubeLines.url, 'line')
  centroids = data.londonCentroids.url

  background = alt.Chart(boroughs).mark_geoshape(stroke='white',
strokeWidth=2).encode(color=alt.value('#eee'),).properties(width=700,height=500)

  labels = alt.Chart(centroids).mark_text().encode(longitude='cx:Q', latitude='cy:Q', text='bLabel:N', size=alt.value(8), opacity=alt.value(0.6)).transform_calculate("bLabel", "indexof (datum.name,' ') > 0  ? substring(datum.name,0,indexof(datum.name, ' ')) : datum.name")

  line_scale = alt.Scale(
        domain=["Bakerloo", "Central", "Circle", "District", "DLR", "Hammersmith & City", "Jubilee", "Metropolitan", "Northern", "Piccadilly", "Victoria", "Waterloo & City" ],
        range=["rgb(137,78,36)", "rgb(220,36,30)", "rgb(255,206,0)", "rgb(1,114,41)", "rgb(0,175,173)", "rgb(215,153,175)", "rgb(106,114,120)", "rgb(114,17,84)", "rgb(0,0,0)", "rgb(0,24,168)", "rgb(0,160,226)", "rgb(106,187,170)"])

  lines = alt.Chart(tubelines).mark_geoshape(filled=False, strokeWidth=2).encode(alt.Color('id:N', legend=alt.Legend(title=None, orient='bottom-right', offset=0)))

  chart = background + labels + lines
  return HttpResponse(chart.to_json(), content_type='application/json')

def gantt_chart(request):
    bokeh_script, bokeh_div = bokeh_chart()
    return render(request, 'maps/gantt_chart.html', {"bokeh_script": bokeh_script, "bokeh_div": bokeh_div})

def shareprice_chart(request):
    #Code to allow user to select the share. Awaiting further refinement
    #if request.method == 'POST':
    #  share = request.POST['drop1']
    #  shares = []
    #  shares += [share]
      shares = ["ULVR.L", "VOD.L", "MNDI.L", "LLOY.L", "RDSB.L", "CLDN.L"] ## "ULVR.L", "VOD.L", "MNDI.L", "LLOY.L", "RDSB.L", "CLDN.L", "FGT.L", "BGS.L", "JESC.L", "HSL.L", "LWDB.L", "SREI.L", "BNKR.L", "SLS.L",  "EBOX.L",
      period = "5d" #1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

      matplotlib_chart = matplotlib_shareprices(shares, period)
      return render(request, 'maps/shareprice_chart.html', {"matplotlib_chart": matplotlib_chart})

    #else:
      return render(request, 'maps/shareprice_chart.html')

class GdUkListedBuildingsListView(ListView):

    #Sets the location to Matlock as an example
    longitude = -1.673260730022491
    latitude = 53.21422845541655
    user_location = Point(longitude, latitude, srid=4326)
    queryset = GdUkListedBuildings.objects.annotate(distance=Distance('geometry', user_location)).order_by('distance')[0:100]
    distance=Distance('geometry', user_location)

def add_markers_to_clusters(shapefile, _marker_cluster, shapefile_type):
    """
    If the shapefile is of points (e.g. listed_buildings) then it can be used directly to set the Folium markers, otherwise create points as the centre of the geometry. Listed buildings also have additional information to include on the label.
    """
    shapefile  = shapefile.to_crs(epsg=4326)
    shapefile.set_index(shapefile.Name,inplace=True)

    if shapefile_type =='listed_buildings':
        coords = [(y,x) for y,x in zip(shapefile['geometry'].y , shapefile['geometry'].x)]
    else:
        shapefile["center"] = shapefile["geometry"].centroid
        shapefile_points = shapefile.copy()
        shapefile_points.set_geometry("center", inplace = True)
        shapefile_points.set_index(shapefile_points.Name,inplace=True)
        coords = [(y,x) for y,x in zip(shapefile_points['center'].y , shapefile_points['center'].x)]

    if shapefile_type == 'always_open_land':
        #National Trust data with no urls to include in labels
        for point in range(0, len(coords)):
            label = str(shapefile_points['Name'][point])
            folium.Marker(location = coords[point], popup= label, tooltip=str(shapefile['Name'][point])).add_to(_marker_cluster)
    elif shapefile_type == 'listed_buildings':
        #For this Historic England dataset the popup label should combine the description and the listing grade
        for point in range(0, len(coords)):
            label_html = folium.Html('<a href="'
                + str(shapefile['Hyperlink'][point])
                + '"target="_blank">'
                + 'Grade:' 
                + str(shapefile['Grade'][point])
                + ' '
                + str(shapefile['Name'][point]) 
                + '</a>', script=True)
            label = folium.Popup(label_html, max_width=2650)
            folium.Marker(location = coords[point], popup= label, tooltip=str(shapefile['Name'][point])).add_to(_marker_cluster)
    else:
        #For Historic England datasets with URL but no listing grade
        for point in range(0, len(coords)):
            label_html = folium.Html('<a href="'
                + str(shapefile['Hyperlink'][point])
                + '"target="_blank">'
                + str(shapefile['Name'][point]) 
                + '</a>', script=True)
            label = folium.Popup(label_html, max_width=2650)
            folium.Marker(location = coords[point], popup= label, tooltip=str(shapefile['Name'][point])).add_to(_marker_cluster)

    #shapefile_info(shapefile)
    return(shapefile)

class HeritageMapView(TemplateView):

    template_name = "maps/heritage_map.html"

    def get_context_data(self, **kwargs):
        county = self.kwargs['county_name']

        if os.environ.get('DATABASE_URL'):
            db_connection_url = os.environ.get('DATABASE_URL')
        else:
            db_connection_url = settings.DATABASE_URL
        con = create_engine(db_connection_url)

        sql = text('SELECT * FROM public."UK_admin_boundaries" WHERE ctyua19nm = :county')      
        county_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})
        county_4326 = county_27700.to_crs(epsg=4326)

        sql = text('SELECT a.* FROM public."gd_UK_scheduled_monuments" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        scheduled_monuments_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        sql = text('SELECT a.* FROM public."gd_UK_parks_gardens" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        parks_gardens_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        sql = text('SELECT a.* FROM public."gd_UK_always_open_land" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        always_open_land_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        sql = text('SELECT a.* FROM public."gd_UK_listed_buildings" as a JOIN public."UK_admin_boundaries" as b ON ST_WITHIN(a.geometry, b.geometry) WHERE b.ctyua19nm = :county')
        listed_buildings_27700 = gpd.GeoDataFrame.from_postgis(sql, con, geom_col="geometry", params={"county":county})

        # Following will throw a warning that the centroids may not be accurate due to the CRS but the inaccuracy is not significant
        figure = folium.Figure()
        m = folium.Map([county_4326.geometry.centroid.y[0], county_4326.geometry.centroid.x[0]], zoom_start= 10, tiles='cartodbpositron', prefer_canvas=True)
        m.add_to(figure)

        #Add clusters and markers to the map
        marker_cluster = MarkerCluster().add_to(m)

        if len(listed_buildings_27700.index) != 0: #Faster than empty or even len(pd)
            listed_buildings_4326 = add_markers_to_clusters(listed_buildings_27700, marker_cluster, 'listed_buildings')

        if len(scheduled_monuments_27700.index) != 0:
            scheduled_monuments_4326 = add_markers_to_clusters(scheduled_monuments_27700, marker_cluster, 'scheduled_monuments')

        if len(parks_gardens_27700.index) != 0:
            parks_gardens_4326 = add_markers_to_clusters(parks_gardens_27700, marker_cluster, 'parks_gardens')
            folium.GeoJson(data=parks_gardens_4326["geometry"]).add_to(m)

        if len(always_open_land_27700.index) != 0:
            always_open_land_4326 = add_markers_to_clusters(always_open_land_27700, marker_cluster, 'always_open_land')
            folium.GeoJson(data=always_open_land_4326["geometry"]).add_to(m)

        figure.render()
        return {"map": figure, "county":county}

class TopicListView(OwnerListView):
   model = Topic

class TopicDetailView(OwnerDetailView):
    model = Topic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #Get the current context data
        context['posts'] = context['topic'].post_set.all()
        return context

@method_decorator(login_required, name='dispatch')
class TopicCreateView(OwnerCreateView): #Convention: topic_form.html
   model = Topic
   fields = ['type', 'text']

@method_decorator(login_required, name='dispatch')
class TopicUpdateView(OwnerUpdateView): #Convention: topic_form.html
   model = Topic
   fields = ['type', 'text'] 

@method_decorator(login_required, name='dispatch')
class TopicDeleteView(OwnerDeleteView): #Convention: topic_confirm_delete.html
   model = Topic

class PostDetailView(OwnerDetailView):
    model = Post

@method_decorator(login_required, name='dispatch')
class PostCreateView(OwnerCreateView): #Convention: post_form.html
   model = Post
   fields = ['title', 'body', 'status', 'url']
   def post(self, request, pk):
    form = PostForm(data=request.POST)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.owner = request.user
        new_post.topic = get_object_or_404(Topic, id=pk)
        new_post.save()
        return redirect(reverse('maps:topic_detail', args=[pk]))

@method_decorator(login_required, name='dispatch')
class PostUpdateView(OwnerUpdateView): #Convention: post_form.html
   model = Post
   fields = ['title', 'body', 'status', 'url']

   def post(self, request, pk):
        post = Post.objects.get(id=pk)
        topic = post.topic
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('maps:topic_detail', args=[topic.id]))

@method_decorator(login_required, name='dispatch')
class PostDeleteView(OwnerDeleteView): #Convention: post_confirm_delete.html
   model = Post

class HeritageSiteListView(ListView):
  model = HeritageSite

class VisitListView(ListView):
  model = Visit

def heritage_site(request, heritage_site_id):
  heritage_site = HeritageSite.objects.get(id=heritage_site_id)
  context = {'heritage_site': heritage_site}
  return render(request, 'maps/heritage_site.html', context)

@login_required
def visit(request, visit_id):
  visit = Visit.objects.get(id=visit_id)
  context = {'visit': visit}
  return render(request, 'maps/visit.html', context)

@login_required
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            cwd = os.getcwd()
            if cwd == '/app' or cwd[:4] == '/tmp':
              app_id = os.environ['EMAIL_ADDRESS']
            else:
              config = configparser.ConfigParser()
              config.read(os.path.join("D:\\MLDatasets", "API_Keys", "TPAMWeb.ini"))
              address = config['Email']['address']
            send_mail(subject, message, address, [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'maps/share.html', {'post': post,'form': form,'sent': sent})

@login_required
def choose_location(request):

    if request.method == 'POST':
        location_list = LocationChoiceField(request.POST)

        if location_list.is_valid():
            selected_location = location_list.cleaned_data['locations']
            county=str(selected_location)
            return HttpResponseRedirect(reverse('maps:heritage_map', args=[county]))
    else:
        location_list = LocationChoiceField()
        errors = location_list.errors or None
        context = {'location_list':location_list, 'errors': errors,}
        return render(request, 'maps/choose_location.html', context)