import csv
import json
import os


def csv_to_json(input_csv_file, output_json_file):
    data = []

    # Read data from the CSV file
    with open(input_csv_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Filter out fields with "NULL" values
            cleaned_row = {
                key: value if value != "NULL" else "" for key, value in row.items()
            }
            data.append(cleaned_row)

    # Write data to a JSON file
    with open(output_json_file, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Usage example:
DATAIO_DIR = os.path.join("D:\\DATA", "TPAM")
input_csv_file = os.path.join(DATAIO_DIR, "references_type_3.csv")
output_json_file = os.path.join(DATAIO_DIR, "references_type_3.json")
csv_to_json(input_csv_file, output_json_file)
