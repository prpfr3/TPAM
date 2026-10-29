#!/usr/bin/env python3
"""Fuzzy-match CSV location values to TPAM Location.name values.

Example:
    python utils/fuzzy_match_locations.py input.csv output.csv --input-column Location
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TPAM.settings")

import django
from fuzzywuzzy import fuzz, process


django.setup()

from locations.models import Location


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def normalize_header(value: str) -> str:
    return (value or "").replace("\ufeff", "").strip().lower()


def detect_delimiter(sample: str) -> str:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        pass

    counts = {delimiter: sample.count(delimiter) for delimiter in [",", ";", "|", "\t"]}
    best_delimiter = max(counts, key=counts.get)
    return best_delimiter if counts[best_delimiter] > 0 else ","


def read_csv_rows(input_path: Path):
    raw_bytes = input_path.read_bytes()
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
    delimiter = detect_delimiter(sample)
    rows = list(csv.reader(lines, delimiter=delimiter))
    if not rows:
        raise ValueError("The input CSV does not contain a header row.")

    headers = [column.replace("\ufeff", "").strip() for column in rows[0]]
    normalized_headers = [normalize_header(column) for column in headers]
    return headers, rows[1:], normalized_headers


def load_location_names() -> Tuple[List[str], dict]:
    records = []
    for name, wikiname, slug in Location.objects.exclude(name__isnull=True).values_list("name", "wikiname", "slug"):
        name_value = str(name or "").strip()
        wiki_value = str(wikiname or "").strip()
        if name_value:
            records.append((name_value, slug or ""))
        if wiki_value:
            records.append((wiki_value, slug or ""))
    names = [name for name, _ in records]
    lookup = {name.lower(): slug for name, slug in records}
    return names, lookup


def find_best_match(value: str, candidates: List[str], min_score: int = 60) -> Tuple[str, int]:
    if not value or not candidates:
        return "", 0

    best_match, score = process.extractOne(
        normalize_text(value),
        candidates,
        scorer=fuzz.token_sort_ratio,
    ) or ("", 0)

    if score is None:
        score = 0

    if score < min_score:
        return "", score

    return best_match, score


def process_csv(input_path: str, output_path: str, input_column: str, output_column: str, score_column: str, place_column: str, latitude_column: str, longitude_column: str, min_score: int) -> None:
    location_names, location_lookup = load_location_names()
    input_path = Path(input_path)
    output_path = Path(output_path)

    headers, data_rows, normalized_headers = read_csv_rows(input_path)
    normalized_input_column = normalize_header(input_column)
    if normalized_input_column not in normalized_headers:
        raise ValueError(
            f"Column '{input_column}' was not found in the input CSV. Available columns: {', '.join(headers)}"
        )

    input_column_index = normalized_headers.index(normalized_input_column)

    fieldnames = list(headers)
    if output_column in fieldnames:
        fieldnames.remove(output_column)
    if score_column in fieldnames:
        fieldnames.remove(score_column)

    fieldnames.extend([output_column, score_column, place_column, latitude_column, longitude_column])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data_rows:
            row_data = {
                header: row[index] if index < len(row) else ""
                for index, header in enumerate(headers)
            }
            raw_value = row_data.get(headers[input_column_index], "")
            normalized_input = raw_value.split(",", 1)[0].strip()
            matched_name, match_score = find_best_match(normalized_input, location_names, min_score=min_score)
            match_details = location_lookup.get(matched_name.lower(), {})
            row_data[output_column] = match_details.get("slug", "")
            row_data[score_column] = match_score
            row_data[place_column] = match_details.get("place", "")
            row_data[latitude_column] = match_details.get("latitude", "")
            row_data[longitude_column] = match_details.get("longitude", "")
            writer.writerow(row_data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fuzzy-match CSV location values against TPAM Location.name values")
    parser.add_argument("input_csv", help="Path to the source CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("--input-column", default="Location", help="Column in the input CSV that contains the location text")
    parser.add_argument("--output-column", default="fuzzy_match", help="Column name to write the matched location into")
    parser.add_argument("--score-column", default="fuzzy_match_score", help="Column name to write the fuzzy match score into")
    parser.add_argument("--place-column", default="fuzzy_match_place", help="Column name to write the matched location place into")
    parser.add_argument("--latitude-column", default="fuzzy_match_latitude", help="Column name to write the matched location latitude into")
    parser.add_argument("--longitude-column", default="fuzzy_match_longitude", help="Column name to write the matched location longitude into")
    parser.add_argument("--min-score", type=int, default=60, help="Minimum fuzzy match score required to write a match")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    process_csv(
        input_path=args.input_csv,
        output_path=args.output_csv,
        input_column=args.input_column,
        output_column=args.output_column,
        score_column=args.score_column,
        place_column=args.place_column,
        latitude_column=args.latitude_column,
        longitude_column=args.longitude_column,
        min_score=args.min_score,
    )
    print(f"Wrote output to {args.output_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
