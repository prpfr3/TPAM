from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *  
import json
import wikipediaapi

def storymaps(request):
    storymaps = SlideHeader.objects.order_by('text_headline')
    paginator = Paginator(storymaps, 20)
    page = request.GET.get('page')
    try:
        storymaps = paginator.page(page)
    except PageNotAnInteger:
        storymaps = paginator.page(1)
    except EmptyPage:
        storymaps = paginator.page(paginator.num_pages)
    context = {'page': page, 'storymaps': storymaps}
    return render(request, 'storymaps/storymaps.html', context)

def storymap(request, storymap_id):

    slideheader = SlideHeader.objects.get(id=storymap_id)
    slides = Slide.objects.filter(slideheader__id=storymap_id).order_by('slidepack__slide_order')

    #Add the first slide to a dictionary list from the SlideHeader Object
    slide_dict = {'location_line': slideheader.location_line, 'media': {}}
    slide_dict['media']['caption'] = slideheader.media_caption
    slide_dict['media']['credit'] = slideheader.media_credit
    slide_dict['media']['url'] = slideheader.media_url
    slide_dict['text'] = {}
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
    page_name = slideheader.wikipedia_name.replace(' ', '_')

    if page_name and wiki_wiki.page(page_name).exists:
        # Retain only the Wikipedia page down to Notes and then add any stored additional text
        text_array = wiki_wiki.page(page_name).text.split('<h2>Notes</h2>')
        text_array = text_array[0].split('<h2>References</h2>')
        slide_dict['text']['text'] = f"<p>From Wikipedia:-</p>{text_array[0]}{slideheader.text_text}"
        slide_dict['text']['headline'] = slideheader.wikipedia_name
    else:
        slide_dict['text']['headline'] = slideheader.text_headline
        slide_dict['text']['text'] = slideheader.text_text

    slide_dict['type'] = slideheader.type
    slide_list = [slide_dict]

    #Add subsequent slides to the dictionary list from the Slide objects
    for slide in slides:
        slide_dict = {'background': {}}
        slide_dict['background']['url'] = slide.background
        slide_dict['location'] = {'lat': slide.northing, 'lon': slide.easting, 'zoom': slide.zoom}
        slide_dict['media'] = {'caption': slide.media_caption, 'credit': slide.media_credit, 'url': slide.media_url}

        wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
        page_name = slide.wikipedia_name.replace(' ', '_')
        if page_name and wiki_wiki.page(page_name).exists:
            text_array = wiki_wiki.page(page_name).text.split('<h2>References</h2>')
            slide_dict['text'] = {'text': text_array[0], 'headline': slide.wikipedia_name}
        else:
            slide_dict['text'] = {'headline': slide.text_headline, 'text': slide.text_text}
        slide_list.append(slide_dict)

    # Create a dictionary in the required JSON format, including the dictionary list of slides
    # map type should accept  "https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png" 
    # but {s} causes a problem, use "a" instead or revert to "osm:standard"
    storymap_dict = {"storymap": 
      {"attribution": "Paul Frost", 
        "call_to_action": True, 
        "call_to_action_text": "Take the Trip", 
        "map_as_image": False, 
        "map_subdomains": "", 
        # "map_type": "https://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
        "map_type": "osm:standard",
        "slides": slide_list,   
        "zoomify": False
      }
    }

    storymap_json = json.dumps(storymap_dict)
    return render(request, 'storymaps/storymap.html', {'storymap_json':storymap_json})