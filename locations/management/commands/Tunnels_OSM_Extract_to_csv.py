import requests
import pandas as pd

# Define the Overpass Turbo query
overpass_query = """
[out:json][timeout:60];
// Define the area of interest (United Kingdom)
area["ISO3166-1"="GB"][admin_level=2]->.searchArea;
// Fetch all railway tunnels in the defined area
(
  way["tunnel"="yes"]["railway"](area.searchArea);
  relation["tunnel"="yes"]["railway"](area.searchArea);
);
// Output the results
out body;
>;
out skel qt;
"""


# Function to execute the Overpass query and return the results
def execute_overpass_query(query):
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.post(overpass_url, data={"data": query})
    response.raise_for_status()
    return response.json()


# Function to process Overpass results and save them to a CSV file
def save_results_to_csv(results, output_file):
    elements = results["elements"]
    data = []

    for element in elements:
        row = {"id": element["id"], "type": element["type"]}
        tags = element.get("tags", {})
        row.update(tags)
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)


# Run the query and save the results
results = execute_overpass_query(overpass_query)
output_file = "D://Data/TPAM/Locations_Tunnels_OSM_Tags.csv"
save_results_to_csv(results, output_file)

print(f"Results have been saved to {output_file}")
