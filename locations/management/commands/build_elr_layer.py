# management/commands/build_elr_layer.py

#To execute this try python manage.py build_elr_layer --tolerance 0.0005 --precision 4

import json
import os
from shapely.geometry import shape, mapping
from django.core.management.base import BaseCommand
from django.conf import settings
from locations.models import ELR  


def simplify_geojson_data(geojson_dict, tolerance=0.0005):
    if "features" not in geojson_dict:
        return geojson_dict
    for feature in geojson_dict["features"]:
        geom = shape(feature["geometry"])
        simplified_geom = geom.simplify(tolerance, preserve_topology=True)
        feature["geometry"] = mapping(simplified_geom)
        props = feature.get("properties", {})
        feature["properties"] = {
            "name": props.get("name") or props.get("ref") or "Unknown",
            "ref": props.get("ref", "")
        }
    return geojson_dict


def truncate_coords(obj, precision=5):
    if isinstance(obj, float):
        return round(obj, precision)
    elif isinstance(obj, dict):
        return {k: truncate_coords(v, precision) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [truncate_coords(x, precision) for x in obj]
    return obj


class Command(BaseCommand):
    help = "Pre-process and cache the ELR GeoJSON layer to a static file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Output file path. Defaults to STATICFILES_DIRS[0]/geojson/elr_layer.json",
        )
        parser.add_argument(
            "--tolerance",
            type=float,
            default=0.0001,
            help="Simplification tolerance in degrees (default: 0.0001 ≈ 11m)",
        )
        parser.add_argument(
            "--precision",
            type=int,
            default=5,
            help="Coordinate decimal precision (default: 5)",
        )

    def handle(self, *args, **options):
        tolerance = options["tolerance"]
        precision = options["precision"]

        # Resolve output path
        output_path = options["output"]
        if not output_path:
            base_dir = settings.STATICFILES_DIRS[0]
            output_path = os.path.join(base_dir, "geojson", "elr_layer.json")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.stdout.write("Fetching ELR data...")
        # Adjust this queryset to match your actual model/fields
        elrs = ELR.objects.exclude(geojson=None).values("geojson")

        all_features = []
        errors = 0

        for elr in elrs:
            if not elr.get("geojson"):
                continue
            try:
                raw_data = elr["geojson"]
                # Handle both JSONField (already a dict) and TextField (needs parsing)
                if isinstance(raw_data, str):
                    raw_data = json.loads(raw_data)
                simplified_data = simplify_geojson_data(raw_data, tolerance=tolerance)
                final_data = truncate_coords(simplified_data, precision)
                all_features.extend(final_data.get("features", []))
            except Exception as e:
                self.stderr.write(f"Error processing ELR: {e}")
                errors += 1

        if not all_features:
            self.stderr.write("No features found. Aborting.")
            return

        combined_geojson = {"type": "FeatureCollection", "features": all_features}

        with open(output_path, "w") as f:
            json.dump(combined_geojson, f, separators=(",", ":"))  # compact output

        feature_count = len(all_features)
        file_size_kb = os.path.getsize(output_path) / 1024
        self.stdout.write(self.style.SUCCESS(
            f"ELR layer saved to {output_path}\n"
            f"  Features : {feature_count}\n"
            f"  File size: {file_size_kb:.1f} KB\n"
            f"  Errors   : {errors}"
        ))