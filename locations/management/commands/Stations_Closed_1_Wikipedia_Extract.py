"""
Extracts Railway Location references from Wikipedia based on pre-specified Wikipedia categories
"""

import requests, csv, os
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import unquote
import string

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = "url"
current_date = datetime.now().strftime("%Y-%m-%d")

OUTPUT_FILE = os.path.join(
    DATAIO_DIR, f"Location_Stations_Closed_Wikipedia_Extract_{current_date}.csv"
)

LOG_FILE = os.path.join(
    DATAIO_DIR, f"Location_Stations_Closed_Wikipedia_Extract_{current_date}.log"
)


def fetch_page(letter, input_type="file"):
    try:
        if URL_OR_FILE == "file":
            url = (
                os.path.join(DATAIO_DIR, "List_of_closed_railway_stations_in_Britain:_")
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
            url = f"https://en.wikipedia.org/wiki/List_of_closed_railway_stations_in_Britain:_{letter}"
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

        tables = soup.find_all("table", {"class": "wikitable"})
        if tables:
            return tables
        else:
            print(f"No table found for letter {letter}")
            return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


with open(OUTPUT_FILE, "wt+", newline="", encoding="utf-8") as csvFile:
    output = csv.writer(csvFile)
    csv_output_row = [
        "Name",
        "Wiki",
        # "Geometry",
        "Company",
        "Company_Wiki",
        "Closed",
        "Ref_Wiki",
        "Note",
        "Note_Attribute",
    ]
    output.writerow(csv_output_row)

    csvLogfile = open(LOG_FILE, "wt+", newline="", encoding="utf-8")
    outputLogfile = csv.writer(csvLogfile)

    alphabet = [
        "A",
        "B",
        "C",
        "D-F",
        "G",
        "H-J",
        "K-L",
        "M-O",
        "P-R",
        "S",
        "T-V",
        "W-Z",
    ]
    # alphabet = ["G"]

    stations_added = 0

    for letter in alphabet:
        tables = fetch_page(letter, input_type=URL_OR_FILE)

        for table in tables:
            trs = table.find_all("tr")

            for tr in trs:
                csv_output_row = []
                csv_logfile_row = []

                for td_id, td in enumerate(tr.find_all(["td"]), start=1):

                    without_line_breaks = td.get_text().replace("\n", "")
                    csv_output_row.append(without_line_breaks)
                    a = td.find("a", href=True)
                    if a:
                        csv_output_row.append(a["href"])
                    else:
                        csv_output_row.append("")

                    # if (
                    #     td_id == 1 and a
                    # ):  # Very occasionally there is no "a" in the first cell
                    #     geometry = ""
                    #     try:
                    #         url_station = "https://en.wikipedia.org" + a["href"]
                    #         res = requests.get(url_station)
                    #         res.raise_for_status()
                    #         soup = BeautifulSoup(res.text, "html.parser")
                    #         if coords_html := soup.find_all("span", {"class": "geo"}):
                    #             coords_split = coords_html[0].text.split(";")
                    #             geometry = f"POINT({coords_split[1].strip()} {coords_split[0].strip()})"
                    #         else:
                    #             csv_logfile_row.append(
                    #                 'No coordinates in Wikipedia (span class="geo") for '
                    #                 + a["href"]
                    #             )
                    #             outputLogfile.writerow(csv_logfile_row)
                    #     except requests.exceptions.ConnectionError as err:
                    #         # eg, no internet
                    #         raise SystemExit(err) from err
                    #     except IndexError:
                    #         csv_output_row.append("")
                    #         csv_logfile_row.append(
                    #             "No url on the page for:-" + a["href"]
                    #         )
                    #         outputLogfile.writerow(csv_logfile_row)
                    #     except requests.exceptions.HTTPError as err:
                    #         # eg, url, server and other errors
                    #         csv_output_row.append("")
                    #         csv_logfile_row.append(
                    #             "http error suggesting no Wikipedia page for:- "
                    #             + a["href"]
                    #         )
                    #         outputLogfile.writerow(csv_logfile_row)
                    #     csv_output_row.append(geometry)

                if csv_output_row:
                    output.writerow(csv_output_row)
                    stations_added += 1

csv_logfile_row.append(f"{stations_added=}")
