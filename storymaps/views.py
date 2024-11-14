from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .utils import *
import json
import wikipediaapi
import urllib


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


def storymap(request, slug):
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
        slide_dict["text"]["text"] = slideheader.post_fk.body
        slide_dict["text"]["headline"] = slideheader.post_fk.title
    elif slideheader.wikipedia_name:
        wikipage = urllib.parse.unquote(
            slideheader.wikipedia_name, encoding="utf-8", errors="replace"
        )
        wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="github/prpfr3 TPAM",
            language="en",
            extract_format=wikipediaapi.ExtractFormat.HTML,
        )
        if wiki_wiki.page(wikipage).exists:
            # text_array = wiki_wiki.page(wikipage).text.split("<h2>Notes</h2>")
            # header_text = text_array[0].split("<h2>References</h2>")
            header_text = wiki_wiki.page(wikipage).summary

        slide_dict["text"]["headline"] = slideheader.wikipedia_name
        slide_dict["text"]["text"] = f"<p>From Wikipedia:-</p>{header_text}"

        # This overrides the previous lines with the full html
        url = f"https://en.wikipedia.org/wiki/{wikipage}"
        slide_dict["text"]["text"] = get_wikipage_html(url)

    slide_dict["type"] = slideheader.type
    slide_list = [slide_dict]

    # Add subsequent slides to the dictionary list from the Slide objects
    for slide in slides:
        slide_dict = {"background": {}}
        slide_dict["background"]["url"] = slide.background
        slide_dict["location"] = {
            "lat": slide.northing,
            "lon": slide.easting,
            "zoom": slide.zoom,
        }
        slide_dict["media"] = {
            "caption": slide.media_caption,
            "credit": slide.media_credit,
            "url": slide.media_url,
        }

        wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="github/prpfr3 TPAM",
            language="en",
            extract_format=wikipediaapi.ExtractFormat.HTML,
        )
        page_name = slide.wikipedia_name.replace(" ", "_")
        if page_name and wiki_wiki.page(page_name).exists:
            text_array = wiki_wiki.page(page_name).text.split("<h2>References</h2>")
            slide_dict["text"] = {
                "text": text_array[0],
                "headline": slide.wikipedia_name,
            }
        else:
            slide_dict["text"] = {
                "headline": slide.text_headline,
                "text": slide.text_text,
            }
        slide_list.append(slide_dict)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    # map type should accept  "https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png"
    # but {s} causes a problem, use "a" instead or revert to "osm:standard"
    storymap_dict = {
        "storymap": {
            "attribution": "Paul Frost",
            "call_to_action": True,
            "call_to_action_text": "Travel the Route",
            "map_as_image": False,
            "map_subdomains": "",
            # See Overlay tab of NLS Maps for map countyoptions
            # "map_type": "https://mapseries-tilesets.s3.amazonaws.com/25_inch/kent/{z}/{x}/{y}.png",
            # "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    storymap_json = json.dumps(storymap_dict)

    return render(request, "storymaps/storymap.html", {"storymap_json": storymap_json})


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


def carousel(request, slug):

    carouselheader = CarouselHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(carousel_slideheader__id=carouselheader.id).order_by(
        "carouselpack__slide_order"
    )

    return render(request, "storymaps/carousel.html", {"slides": slides})


def timelines(request):
    timelines = TimelineSlideHeader.objects.order_by("text_headline")
    timelines = TimelineSlideHeader.objects.all()

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


def timeline(request, slug):
    slideheader = TimelineSlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(timeline_slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    tdict = {
        "title": {
            "media": {"url": "", "caption": "", "credit": ""},
            "text": {
                "headline": "",
                "text": "",
            },
        },
        "events": [],
    }
    # Add the first slide to a dictionary list from the TimelineSlideHeader Object
    tdict["title"]["media"]["caption"] = slideheader.media_caption
    tdict["title"]["media"]["credit"] = slideheader.media_credit
    tdict["title"]["media"]["url"] = slideheader.media_url
    tdict["title"]["text"] = {}
    wiki_wiki = wikipediaapi.Wikipedia(
        language="en",
        user_agent="prpfr3/Github TPAM",
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    page_name = slideheader.wikipedia_name.replace(" ", "_")

    if page_content := get_wikipedia_page_content(page_name):
        # Retain only the Wikipedia page down to Notes and then add any stored additional text
        # text_array = wiki_wiki.page(page_name).text.split("<h2>Notes</h2>")
        # print(text_array)
        # text_array = text_array[0].split("<h2>References</h2>")
        # tdict["title"]["text"][
        #     "text"
        # ] = f"<p>From Wikipedia:-</p>{text_array[0]}{slideheader.text_text}"
        page_content = page_content.replace("/wiki/", "https://en.wikipedia.org/wiki/")
        page_content = page_content.replace(">edit<", "><")
        page_content = page_content.replace(">[<", "><")
        page_content = page_content.replace(">]<", "><")
        tdict["title"]["text"]["text"] = page_content
        tdict["title"]["text"]["headline"] = slideheader.wikipedia_name
    else:
        tdict["title"]["text"]["headline"] = slideheader.text_headline
        tdict["title"]["text"]["text"] = slideheader.text_text

    tdict["type"] = slideheader.type

    # Add subsequent slides to the dictionary list from the TimelineSlide objects
    for slide in slides:
        event = {
            "media": {
                "url": slide.media_url,
                "caption": slide.media_caption,
                "credit": slide.media_credit,
            },
            "start_date": {"year": slide.start_date[:4]},
            "end_date": {"year": slide.end_date[:4]},
        }

        page_name = slide.wikipedia_name.replace(" ", "_")
        if page_name and wiki_wiki.page(page_name).exists:
            text_array = wiki_wiki.page(page_name).text.split("<h2>References</h2>")
            event["text"] = {
                "text": text_array[0],
                "headline": slide.wikipedia_name,
            }
        else:
            event["text"] = {
                "headline": slide.text_headline,
                "text": slide.text_text,
            }
        tdict["events"].append(event)

    timeline_json = json.dumps(tdict)
    return render(request, "storymaps/timeline.html", {"timeline_json": timeline_json})
