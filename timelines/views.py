from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
import wikipediaapi

from .models import *
from .utils import *


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
    context = {"page": page, "timelines": timelines}
    return render(request, "timelines/timelines.html", context)


def timeline(request, slug):
    slideheader = TimelineSlideHeader.objects.get(slug=slug)
    slides = TimelineSlide.objects.filter(slideheader__id=slideheader.id).order_by(
        "timelineslidepack__slide_order"
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
    # wiki_wiki = wikipediaapi.Wikipedia(
    #     # user_agent="TPAM Django Project @ https://github.com/prpfr3", #version 0.6.0 onwards
    #     language="en",
    #     extract_format=wikipediaapi.ExtractFormat.HTML,
    # )
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
    slide_list = [tdict]

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

        wiki_wiki = wikipediaapi.Wikipedia(
            language="en", extract_format=wikipediaapi.ExtractFormat.HTML
        )
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

    return render(request, "timelines/timeline.html", {"timeline_json": timeline_json})
