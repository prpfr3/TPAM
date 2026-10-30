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
    # slides_payload = build_leaflet_storymap_payload(slideheader, slides)
    # return render(
    #     request,
    #     "storymaps/newstorymap.html",
    #     {"slides_payload": json.dumps(slides_payload)},
    # )


def convert_bng_to_wgs84(easting, northing):
    """Convert British National Grid eastings/northings (EPSG:27700) to WGS84 lat/lon."""
    if easting is None or northing is None:
        return None, None
    try:
        from pyproj import Transformer

        transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
        lon, lat = transformer.transform(easting, northing)
        return lat, lon
    except Exception:
        return None, None


def build_leaflet_storymap_payload(slideheader, slides):
    """Construct a Leaflet-friendly payload for the new storymap carousel."""
    header_text = get_text_content(slideheader)
    first_slide = {
        "type": "overview",
        "headline": header_text.get("headline"),
        "text": header_text.get("text"),
        "media_url": get_media_dict(slideheader).get("url"),
        "media_caption": get_media_dict(slideheader).get("caption"),
        "media_credit": get_media_dict(slideheader).get("credit"),
        "lat": None,
        "lon": None,
        "zoom": None,
    }

    slide_payload = [first_slide]
    bounds = [None, None, None, None]
    for slide in slides:
        text = get_text_content(slide)
        media = get_media_dict(slide)
        lat, lon = convert_bng_to_wgs84(slide.easting, slide.northing)
        if lat is not None and lon is not None:
            if bounds[0] is None or lat < bounds[0]:
                bounds[0] = lat
            if bounds[1] is None or lon < bounds[1]:
                bounds[1] = lon
            if bounds[2] is None or lat > bounds[2]:
                bounds[2] = lat
            if bounds[3] is None or lon > bounds[3]:
                bounds[3] = lon

        slide_payload.append(
            {
                "type": "location",
                "headline": text.get("headline"),
                "text": text.get("text"),
                "media_url": media.get("url"),
                "media_caption": media.get("caption"),
                "media_credit": media.get("credit"),
                "lat": lat,
                "lon": lon,
                "zoom": slide.zoom or 12,
            }
        )

    bounds_payload = None
    if bounds[0] is not None:
        bounds_payload = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]

    return {
        "attribution": "© OpenStreetMap contributors",
        "tiles": {
            "url": settings.MAP_TILE_URL,
            "attribution": settings.MAP_TILE_ATTRIBUTION,
        },
        "slides": slide_payload,
        "bounds": bounds_payload,
    }


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


def proxy_tile(request, z, x, y):
    """
    Proxy view for tile requests that adds proper User-Agent and Referer headers
    to satisfy OpenStreetMap's tile usage policy.
    """
    import requests
    from django.http import HttpResponse

    # Construct the tile URL
    tile_url = (
        settings.MAP_TILE_URL.replace("{z}", str(z))
        .replace("{x}", str(x))
        .replace("{y}", str(y))
        .replace("{s}", "a")
    )

    # Identify the application and provide a referrer for OSM tile requests.
    headers = {
        "User-Agent": "TPAM/1.0 (+https://github.com/prpfr3/TPAM)",
        "Referer": request.build_absolute_uri("/"),
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    try:
        response = requests.get(tile_url, headers=headers, timeout=15)

        if response.status_code == 200:
            # print(
            #     f"Tile proxy success: {response.status_code}, content-type: {response.headers.get('content-type')}"
            # )
            return HttpResponse(
                response.content,
                content_type=response.headers.get("content-type", "image/png"),
                headers={
                    "Cache-Control": "public, max-age=86400",  # Cache tiles for 24 hours
                },
            )
        else:
            # print(
            #     f"Tile proxy failed: {response.status_code}, response: {response.text[:200]}"
            # )
            return HttpResponse(status=response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Tile proxy error: {e}")
        return HttpResponse(status=500)
