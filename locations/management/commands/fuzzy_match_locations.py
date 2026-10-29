import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from fuzzywuzzy import fuzz, process

from locations.models import Location

# To execute this command, use:
# python manage.py fuzzy_match_locations <input_csv> <output_csv> [--input-column <input_column>] [--output-column <output_column>] [--score-column <score_column>] [--min-score <min_score>]


class Command(BaseCommand):
    help = "Fuzzy-match CSV location values against Location.name"

    def add_arguments(self, parser):
        parser.add_argument("input_csv", help="Path to the input CSV file")
        parser.add_argument("output_csv", help="Path to the output CSV file")
        parser.add_argument(
            "--input-column",
            default="Location",
            help="Column in the input CSV that contains the location text",
        )
        parser.add_argument(
            "--output-column",
            default="fuzzy_match",
            help="Column name to write the matched location into",
        )
        parser.add_argument(
            "--score-column",
            default="fuzzy_match_score",
            help="Column name to write the fuzzy match score into",
        )
        parser.add_argument(
            "--place-column",
            default="fuzzy_match_place",
            help="Column name to write the matched location place into",
        )
        parser.add_argument(
            "--latitude-column",
            default="fuzzy_match_latitude",
            help="Column name to write the matched location latitude into",
        )
        parser.add_argument(
            "--longitude-column",
            default="fuzzy_match_longitude",
            help="Column name to write the matched location longitude into",
        )
        parser.add_argument(
            "--min-score",
            type=int,
            default=60,
            help="Minimum fuzzy match score required to write a match",
        )

    def normalize_header(self, value):
        return (value or "").replace("\ufeff", "").strip().lower()

    def detect_delimiter(self, sample):
        try:
            return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
        except csv.Error:
            pass

        counts = {delimiter: sample.count(delimiter) for delimiter in [",", ";", "|", "\t"]}
        best_delimiter = max(counts, key=counts.get)
        return best_delimiter if counts[best_delimiter] > 0 else ","

    def read_csv_rows(self, input_csv):
        raw_bytes = input_csv.read_bytes()
        encodings = ("utf-8-sig", "utf-16", "utf-16le", "utf-16be", "cp1252", "latin-1")

        text = None
        for encoding in encodings:
            try:
                text = raw_bytes.decode(encoding)
                break
            except UnicodeDecodeError:
                continue

        if text is None:
            raise ValueError("Could not decode the input CSV file.")

        lines = text.splitlines()
        if not lines:
            raise ValueError("The input CSV does not contain any rows.")

        sample = "\n".join(lines[:10])
        delimiter = self.detect_delimiter(sample)
        rows = list(csv.reader(lines, delimiter=delimiter))

        if not rows:
            raise ValueError("The input CSV does not contain a header row.")

        headers = [column.replace("\ufeff", "").strip() for column in rows[0]]
        normalized_headers = [self.normalize_header(column) for column in headers]
        data_rows = rows[1:]
        return headers, data_rows, normalized_headers

    def handle(self, *args, **options):
        input_csv = Path(options["input_csv"]).expanduser().resolve()
        output_csv = Path(options["output_csv"]).expanduser().resolve()
        input_column = options["input_column"]
        output_column = options["output_column"]
        score_column = options["score_column"]
        place_column = options["place_column"]
        latitude_column = options["latitude_column"]
        longitude_column = options["longitude_column"]
        min_score = options["min_score"]

        if not input_csv.exists():
            raise FileNotFoundError(f"Input CSV not found: {input_csv}")

        location_records = list(
            Location.objects.exclude(name__isnull=True).values_list("name", "wikiname", "slug", "RCH_StopsGB_Place", "geometry")
        )
        cleaned_names = []
        location_lookup = {}
        for name, wikiname, slug, place_value, geometry in location_records:
            name_value = str(name or "").strip()
            wiki_value = str(wikiname or "").strip()
            if name_value:
                cleaned_names.append(name_value)
                location_lookup[name_value.lower()] = {
                    "slug": slug or "",
                    "place": str(place_value or "").strip(),
                    "latitude": None,
                    "longitude": None,
                }
            if wiki_value:
                cleaned_names.append(wiki_value)
                location_lookup[wiki_value.lower()] = {
                    "slug": slug or "",
                    "place": str(place_value or "").strip(),
                    "latitude": None,
                    "longitude": None,
                }

            if geometry:
                try:
                    if hasattr(geometry, "y") and hasattr(geometry, "x"):
                        latitude = geometry.y
                        longitude = geometry.x
                    else:
                        latitude = None
                        longitude = None
                except Exception:
                    latitude = None
                    longitude = None

                if name_value:
                    location_lookup[name_value.lower()].update({"latitude": latitude, "longitude": longitude})
                if wiki_value:
                    location_lookup[wiki_value.lower()].update({"latitude": latitude, "longitude": longitude})

        headers, data_rows, normalized_headers = self.read_csv_rows(input_csv)
        normalized_input_column = self.normalize_header(input_column)
        if normalized_input_column not in normalized_headers:
            available = ", ".join(headers)
            raise ValueError(
                f"Column '{input_column}' was not found in the input CSV. Available columns: {available}"
            )

        input_column_index = normalized_headers.index(normalized_input_column)

        fieldnames = list(headers)
        if output_column in fieldnames:
            fieldnames.remove(output_column)
        if score_column in fieldnames:
            fieldnames.remove(score_column)
        if place_column in fieldnames:
            fieldnames.remove(place_column)
        if latitude_column in fieldnames:
            fieldnames.remove(latitude_column)
        if longitude_column in fieldnames:
            fieldnames.remove(longitude_column)
        fieldnames.extend([output_column, score_column, place_column, latitude_column, longitude_column])

        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with output_csv.open("w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            processed = 0
            for row in data_rows:
                row_data = {
                    header: row[index] if index < len(row) else ""
                    for index, header in enumerate(headers)
                }
                raw_value = row_data.get(headers[input_column_index], "")
                matched_slug = ""
                matched_place = ""
                matched_latitude = ""
                matched_longitude = ""
                match_score = 0

                if raw_value and cleaned_names:
                    normalized_input = raw_value.split(",", 1)[0].strip()
                    if normalized_input:
                        best_match, score = process.extractOne(
                            normalized_input.lower(),
                            [name.lower() for name in cleaned_names],
                            scorer=fuzz.token_sort_ratio,
                        ) or ("", 0)
                        if score is None:
                            score = 0
                        if score >= min_score:
                            match_details = location_lookup.get(best_match.lower(), {})
                            matched_slug = match_details.get("slug", "")
                            matched_place = match_details.get("place", "")
                            matched_latitude = match_details.get("latitude", "")
                            matched_longitude = match_details.get("longitude", "")
                            match_score = score

                row_data[output_column] = matched_slug
                row_data[score_column] = match_score
                row_data[place_column] = matched_place
                row_data[latitude_column] = matched_latitude
                row_data[longitude_column] = matched_longitude
                writer.writerow(row_data)
                processed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processed {processed} rows and wrote {output_csv}"
            )
        )
