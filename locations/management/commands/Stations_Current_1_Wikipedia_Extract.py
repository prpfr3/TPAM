"""
Extracts Railway Location references from Wikipedia based on pre-specified Wikipedia categories
"""

import requests, csv, os
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote
import string

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = "url"
current_date = datetime.now().strftime("%Y-%m-%d")

OUTPUT_FILE = os.path.join(
    DATAIO_DIR, f"Location_Stations_Current_Wikipedia_Extract_{current_date}.csv"
)


def fetch_page(letter, input_type="file"):
    try:
        if URL_OR_FILE == "file":
            url = (
                os.path.join(DATAIO_DIR, "Wikipedia_Stations_")
                + letter.lower()
                + ".html"
            )
            try:
                with open(url) as file:
                    soup = BeautifulSoup(file, "html.parser")
            except FileNotFoundError:
                print(f"No local file found for letter {letter}")
                return None
        else:
            url = f"https://en.wikipedia.org/wiki/UK_railway_stations_-_{letter}"
            try:
                print("Trying ", url)
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes
                decoded_content = unquote(response.content.decode("utf-8", "ignore"))
                soup = BeautifulSoup(decoded_content, "html.parser")
            except requests.exceptions.ConnectionError as err:
                print(f"Connection error: {err}")
                return None
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 404:
                    print(f"Page not found for letter {letter}")
                else:
                    print(f"HTTP error occurred: {err}")
                return None
            except requests.exceptions.RequestException as err:
                print(f"An error occurred: {err}")
                return None

        table = soup.find_all("table", {"class": "wikitable"})
        if table:
            return table[0]
        else:
            print(f"No table found for letter {letter}")
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


with open(OUTPUT_FILE, "wt+", newline="", encoding="utf-8") as csvFile:
    output = csv.writer(csvFile)
    csvRow = [
        "NameSlug",
        "Name",
        "Postcode",
        "Code1",
        "Code2",
    ]
    output.writerow(csvRow)

    for letter in string.ascii_uppercase:
        table = fetch_page(letter, input_type=URL_OR_FILE)
        if table:
            rows = table.find_all("tr")

            for row in rows:
                csvRow = []

                first_href_added = False

                for cell in row.find_all("td"):
                    if not first_href_added:
                        if a := cell.find("a", href=True):
                            csvRow.append(a["href"])
                            first_href_added = True
                        else:
                            csvRow.append("")

                for cell in row.find_all("td"):
                    csvRow.append(cell.get_text(strip=True))

                if csvRow:
                    output.writerow(csvRow)
        else:
            print(f"No table or page for letter {letter}")
