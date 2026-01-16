from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import *
from .utils import *
import json
import wikipediaapi
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


def storymap(request, slug):
    import urllib.parse

    slideheader = SlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    # Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict = {"location_line": slideheader.location_line, "media": {}}
    slide_dict["media"]["caption"] = slideheader.media_caption
    slide_dict["media"]["credit"] = slideheader.media_credit
    slide_dict["media"]["url"] = slideheader.media_url
    slide_dict["text"] = {}
    slide_dict["text"]["headline"] = slideheader.text_headline or None
    slide_dict["text"]["text"] = None

    if slideheader.post_fk:
        slide_dict["text"]["headline"] = slideheader.post_fk.title
        slide_dict["text"]["text"] = slideheader.post_fk.body
    elif slideheader.wikipedia_name:
        wikipage = urllib.parse.unquote(
            slideheader.wikipedia_name, encoding="utf-8", errors="replace"
        )
        url = f"https://en.wikipedia.org/wiki/{wikipage}"

        slide_dict["text"]["headline"] = slideheader.wikipedia_name
        slide_dict["text"]["text"] = get_wikipedia_summary(url)
        slide_dict["type"] = slideheader.type
        slide_list = [slide_dict]

    for slide in slides:
        slide_dict = {
            "background": {"url": slide.background},
            "location": {
                "lat": slide.northing,
                "lon": slide.easting,
                "zoom": slide.zoom,
            },
            "media": {
                "caption": slide.media_caption,
                "credit": slide.media_credit,
                "url": slide.media_url,
            },
        }

        slide_dict["text"] = {}
        slide_dict["text"]["headline"] = slide.text_headline or None
        slide_dict["text"]["text"] = slide.notes or None

        # Determine alternative headline and text content
        if slide.post_fk:  # Use the post if available
            slide_dict["text"]["headline"] = slide.post_fk.title
            slide_dict["text"]["text"] = slide.post_fk.body
        elif slide.wikipedia_name:  # Fallback to Wikipedia summary
            slide_dict["text"]["headline"] = slide.wikipedia_name
            wikislug = urllib.parse.unquote(slide.wikipedia_name.replace(" ", "_"))
            url = f"https://en.wikipedia.org/wiki/{wikislug}"
            slide_dict["text"]["text"] = get_wikipedia_summary(url)

        slide_list.append(slide_dict)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    storymap_dict = {
        "storymap": {
            "attribution": "Wikipedia / OpenStreetMaps",
            "call_to_action": True,
            "call_to_action_text": "Up and Down the Line",
            "map_as_image": False,
            "map_subdomains": "",
            # "map_type": "https://mapseries-tilesets.s3.amazonaws.com/25_inch/yorkshire/{z}/{x}/{y}.png",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    storymap_json = json.dumps(storymap_dict)
    return render(request, "storymaps/storymap.html", {"storymap_json": storymap_json})


def timeline(request, slug):
    import urllib.parse

    slideheader = TimelineSlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(timeline_slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    # Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict = {"media": {}}
    slide_dict["media"]["caption"] = slideheader.media_caption
    slide_dict["media"]["credit"] = slideheader.media_credit
    slide_dict["media"]["url"] = slideheader.media_url
    slide_dict["text"] = {}
    slide_dict["text"]["headline"] = slideheader.text_headline or None
    slide_dict["text"]["text"] = None

    # if slideheader.post_fk:
    #     slide_dict["text"]["headline"] = slideheader.post_fk.title
    #     slide_dict["text"]["text"] = slideheader.post_fk.body
    if slideheader.wikipedia_name:
        wikipage = urllib.parse.unquote(
            slideheader.wikipedia_name, encoding="utf-8", errors="replace"
        )
        url = f"https://en.wikipedia.org/wiki/{wikipage}"

        slide_dict["text"]["headline"] = slideheader.wikipedia_name
        slide_dict["text"]["text"] = get_wikipedia_summary(url)
        slide_dict["type"] = slideheader.type
        slide_list = [slide_dict]

    slide_dict["events"] = None

    for slide in slides:

        if not slide.media_url:
            return None

        # Check if it's an absolute URL (e.g. starts with http:// or https://)
        if bool(urlparse(slide.media_url).netloc):
            media_url = slide.media_url  # external URL, return as is
        else:

            # Otherwise, it's a relative path — prepend MEDIA_URL
            media_url = urljoin(settings.MEDIA_URL, slide.media_url)

        slide_dict = {
            "background": {"url": slide.background},
            "media": {
                "url": media_url,
                "caption": slide.media_caption,
                "credit": slide.media_credit,
            },
            "start_date": {"year": slide.start_date[:4]},
            "end_date": {"year": slide.end_date[:4]},
        }

        slide_dict["text"] = {}
        slide_dict["text"]["headline"] = slide.text_headline or None
        slide_dict["text"]["text"] = slide.notes or None

        # Determine alternative headline and text content
        if slide.post_fk:  # Use the post if available
            slide_dict["text"]["headline"] = slide.post_fk.title
            slide_dict["text"]["text"] = slide.post_fk.body
        elif slide.wikipedia_name:  # Fallback to Wikipedia summary
            slide_dict["text"]["headline"] = slide.wikipedia_name
            wikislug = urllib.parse.unquote(slide.wikipedia_name.replace(" ", "_"))
            url = f"https://en.wikipedia.org/wiki/{wikislug}"
            slide_dict["text"]["text"] = get_wikipedia_summary(url)
        slide_list["events"].append(slide_dict)

    timeline_json = json.dumps(slide_list)
    return render(request, "storymaps/timeline.html", {"timeline_json": timeline_json})


def carousel(request, slug):

    carouselheader = CarouselHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(carousel_slideheader__id=carouselheader.id).order_by(
        "carouselpack__slide_order"
    )

    return render(request, "storymaps/carousel.html", {"slides": slides})
