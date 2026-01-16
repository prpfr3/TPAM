from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import *
from .utils import *
import json
import urllib
from urllib.parse import urljoin, urlparse


def storymaps(request):
    storymaps = SlideHeader.objects.order_by("text_headline")
    paginator = Paginator(storymaps, 20)
    page = request.GET.get("page")
    try:
        storymaps = paginator.page(page)
    except PageNotAnInteger:
        storymaps = paginator.page(1)
    except EmptyPage:
        storymaps = paginator.page(paginator.num_pages)
    context = {"storymaps": storymaps}
    return render(request, "storymaps/storymaps.html", context)


def timelines(request):
    timelines = TimelineSlideHeader.objects.order_by("text_headline")

    paginator = Paginator(timelines, 20)
    page = request.GET.get("page")
    try:
        timelines = paginator.page(page)
    except PageNotAnInteger:
        timelines = paginator.page(1)
    except EmptyPage:
        timelines = paginator.page(paginator.num_pages)
    context = {"timelines": timelines}
    return render(request, "storymaps/timelines.html", context)


def carousels(request):
    storymaps = CarouselHeader.objects.order_by("header_text")
    paginator = Paginator(storymaps, 20)
    page = request.GET.get("page")
    try:
        storymaps = paginator.page(page)
    except PageNotAnInteger:
        storymaps = paginator.page(1)
    except EmptyPage:
        storymaps = paginator.page(paginator.num_pages)
    context = {"storymaps": storymaps}
    return render(request, "storymaps/carousels.html", context)


def get_text_content(obj):
    """Return headline and text from post_fk, Wikipedia, or model fields."""
    text = {"headline": obj.text_headline or None, "text": None}

    if getattr(obj, "post_fk", None):
        text["headline"] = obj.post_fk.title
        text["text"] = obj.post_fk.body

    elif getattr(obj, "wikipedia_name", None):
        wikipage = urllib.parse.unquote(
            obj.wikipedia_name.replace(" ", "_"), encoding="utf-8"
        )
        url = f"https://en.wikipedia.org/wiki/{wikipage}"
        text["headline"] = obj.wikipedia_name
        text["text"] = get_wikipedia_summary(url)

    elif getattr(obj, "notes", None):
        text["text"] = obj.notes

    return text


def get_media_dict(obj, use_absolute_url=False):
    """Builds a media dictionary, converting URLs if needed."""
    media_url = obj.media_url
    if use_absolute_url and media_url:
        if not bool(urlparse(media_url).netloc):  # relative path
            media_url = urljoin(settings.MEDIA_URL, media_url)

    return {
        "url": media_url,
        "caption": obj.media_caption,
        "credit": obj.media_credit,
    }


def build_slide(slide):
    """Builds a standard storymap slide dictionary."""
    slide_dict = {
        "background": {"url": slide.background},
        "location": {
            "lat": slide.northing,
            "lon": slide.easting,
            "zoom": slide.zoom,
        },
        "media": get_media_dict(slide),
        "text": get_text_content(slide),
    }
    return slide_dict


def build_timeline_event(slide):
    """Builds a standard timeline event dictionary."""
    media = get_media_dict(slide, use_absolute_url=True)
    event = {
        "background": {"url": slide.background},
        "media": media,
        "start_date": {"year": slide.start_date[:4]},
        "end_date": {"year": slide.end_date[:4]},
        "text": get_text_content(slide),
    }
    return event


def storymap(request, slug):
    slideheader = SlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    # First slide (header info)
    first_slide = {
        "location_line": slideheader.location_line,
        "media": get_media_dict(slideheader),
        "text": get_text_content(slideheader),
        "type": getattr(slideheader, "type", None),
    }

    slide_list = [first_slide]
    slide_list.extend(build_slide(slide) for slide in slides)

    storymap_dict = {
        "storymap": {
            "attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "Up and Down the Line",
            "map_as_image": False,
            "map_subdomains": "",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    storymap_json = json.dumps(storymap_dict)
    return render(request, "storymaps/storymap.html", {"storymap_json": storymap_json})


def timeline(request, slug):
    slideheader = TimelineSlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(timeline_slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    # First slide (header info)
    slide_dict = {
        "media": get_media_dict(slideheader),
        "text": get_text_content(slideheader),
        "events": [],
    }

    for slide in slides:
        if not slide.media_url:
            continue  # skip incomplete slides

        slide_dict["events"].append(build_timeline_event(slide))

    timeline_json = json.dumps(slide_dict)
    return render(request, "storymaps/timeline.html", {"timeline_json": timeline_json})


def carousel(request, slug):

    carouselheader = CarouselHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(carousel_slideheader__id=carouselheader.id).order_by(
        "carouselpack__slide_order"
    )

    return render(request, "storymaps/carousel.html", {"slides": slides})