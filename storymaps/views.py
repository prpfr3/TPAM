from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
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
    context = {"page": page, "storymaps": storymaps}
    return render(request, "storymaps/storymaps.html", context)


import requests
from bs4 import BeautifulSoup


def get_wikipage_html(url):
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the <div> tag with id=bodyContent
    body_content_div = soup.find("div", id="bodyContent")

    if body_content_div:

        # Remove mw-editsection and its descendants
        for element in body_content_div.select(".mw-editsection"):
            element.decompose()

        # Remove mw-editsection and its descendants
        for element in body_content_div.select(".box-More_citations_needed"):
            element.decompose()

        # Split the HTML content within the bodyContent div at the point where <div class="navbox-styles"> occurs
        split_html = str(body_content_div).split('<div class="navbox-styles">')

        # Keep only the first part of the split, which contains the content before navbox-styles
        html_within_body_content = (
            split_html[0]
            .replace("<span>edit<span>", "")
            .replace("/wiki/", "https://en.wikipedia.org/wiki/")
        )

        return html_within_body_content
    else:
        print("No <div> tag with id=bodyContent found.")
        return None


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
            # "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
            "map_type": "osm:standard",
            "slides": slide_list,
            "zoomify": False,
        }
    }

    storymap_json = json.dumps(storymap_dict)

    return render(request, "storymaps/storymap.html", {"storymap_json": storymap_json})


def carousels(request):
    storymaps = SlideHeader.objects.order_by("text_headline")
    paginator = Paginator(storymaps, 20)
    page = request.GET.get("page")
    try:
        storymaps = paginator.page(page)
    except PageNotAnInteger:
        storymaps = paginator.page(1)
    except EmptyPage:
        storymaps = paginator.page(paginator.num_pages)
    context = {"page": page, "storymaps": storymaps}
    return render(request, "storymaps/carousels.html", context)


def carousel(request, slug):

    slideheader = SlideHeader.objects.get(slug=slug)
    slides = Slide.objects.filter(slideheader__id=slideheader.id).order_by(
        "slidepack__slide_order"
    )

    return render(request, "storymaps/carousel.html", {"slides": slides})
