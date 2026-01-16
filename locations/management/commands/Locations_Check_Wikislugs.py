import csv
import time
import requests
from pathlib import Path

from django.core.management.base import BaseCommand
from locations.models import Location  # <- change to your actual app/model

HEADERS = {"User-Agent": "MyWikiChecker/1.0 (paul.frost@talktalk.net)"}


def _wikipedia_batch_query(titles):
    """Query Wikipedia API for a list of titles (underscores)."""
    if not titles:
        return {}

    api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles),
        "redirects": 1,
    }

    r = requests.get(api, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    query = data.get("query", {})
    redirects = query.get("redirects", [])
    pages = query.get("pages", {})

    redirect_map = {rd["from"].replace(" ", "_"): rd["to"] for rd in redirects}
    existing = set()
    for p in pages.values():
        if "missing" not in p:
            existing.add(p.get("title").replace(" ", "_"))

    results = {}
    for t in titles:
        entry = {
            "query_title": t,
            "exists": False,
            "is_redirect": False,
            "target_title": "",
        }
        if t in redirect_map:
            entry["exists"] = True
            entry["is_redirect"] = True
            entry["target_title"] = redirect_map[t].replace(" ", "_")
        elif t in existing:
            entry["exists"] = True
            entry["is_redirect"] = False
            entry["target_title"] = t
        results[t] = entry
    return results


class Command(BaseCommand):
    help = "Check Wikipedia pages for Location.wikiname"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="wikipedia_check_results.csv",
            help="Output CSV file path",
        )
        parser.add_argument(
            "--batch_size",
            type=int,
            default=50,
            help="Number of titles per batch",
        )
        parser.add_argument(
            "--pause",
            type=float,
            default=1.0,
            help="Pause in seconds between batches",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        batch_size = options["batch_size"]
        pause = options["pause"]

        qs = (
            Location.objects.exclude(wikiname__isnull=True)
            .exclude(wikiname="")
            .order_by("id")
        )
        items = [(obj, obj.wikiname.strip()) for obj in qs]

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "id",
                    "wikiname",
                    "query_title",
                    "fallback_used",
                    "exists",
                    "is_redirect",
                    "target_slug",
                ]
            )

            for i in range(0, len(items), batch_size):
                batch = items[i : i + batch_size]
                primary_titles = [
                    wikiname.replace(" ", "_") + "_railway_station"
                    for _, wikiname in batch
                ]
                primary_results = _wikipedia_batch_query(primary_titles)

                fallback_needed = []
                for idx, primary in enumerate(primary_titles):
                    pr = primary_results.get(primary)
                    if not pr or not pr["exists"]:
                        fallback_needed.append(idx)

                fallback_results = {}
                if fallback_needed:
                    fallback_titles = [
                        batch[idx][1].replace(" ", "_") for idx in fallback_needed
                    ]
                    fb_query_results = _wikipedia_batch_query(fallback_titles)
                    for j, idx in enumerate(fallback_needed):
                        fb_title = fallback_titles[j]
                        fallback_results[idx] = fb_query_results.get(
                            fb_title,
                            {
                                "query_title": fb_title,
                                "exists": False,
                                "is_redirect": False,
                                "target_title": "",
                            },
                        )

                # Prepare rows and write only if redirect OR missing
                for idx, (obj, wikiname) in enumerate(batch):
                    primary = primary_titles[idx]
                    prim_res = primary_results.get(
                        primary,
                        {
                            "query_title": primary,
                            "exists": False,
                            "is_redirect": False,
                            "target_title": "",
                        },
                    )

                    if prim_res["exists"]:
                        final = {
                            "query_title": prim_res["query_title"],
                            "fallback_used": False,
                            "exists": prim_res["exists"],
                            "is_redirect": prim_res["is_redirect"],
                            "target_slug": prim_res["target_title"],
                        }
                    else:
                        fb = fallback_results.get(idx)
                        if fb and fb.get("exists"):
                            final = {
                                "query_title": fb["query_title"],
                                "fallback_used": True,
                                "exists": fb["exists"],
                                "is_redirect": fb["is_redirect"],
                                "target_slug": fb["target_title"],
                            }
                        else:
                            final = {
                                "query_title": primary,
                                "fallback_used": idx in fallback_results,
                                "exists": False,
                                "is_redirect": False,
                                "target_slug": "",
                            }

                    # Only write row if redirect or missing
                    if final["is_redirect"] or not final["exists"]:
                        writer.writerow(
                            [
                                obj.pk,
                                wikiname,
                                final["query_title"],
                                final["fallback_used"],
                                final["exists"],
                                final["is_redirect"],
                                final["target_slug"],
                            ]
                        )

                time.sleep(pause)

        self.stdout.write(self.style.SUCCESS(f"CSV written to {output_path}"))
