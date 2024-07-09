import requests, os
from bs4 import BeautifulSoup

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
URL_OR_FILE = "file"
url = f"http://www.railwaycodes.org.uk/elrs/_mileages/s/xtd.shtm"

output_file = os.path.join(DATAIO_DIR, "ELR_XTD.csv")
with open(output_file, "wt+", newline="", encoding="utf-8") as csvFile:

    if URL_OR_FILE == "file":
        url = os.path.join(DATAIO_DIR, "ELR_XTD.html")
        soup = BeautifulSoup(open(url), "html.parser")
    else:
        try:
            response = requests.get(url).content.decode("utf-8", "ignore")
        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err) from err
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err) from err

        soup = BeautifulSoup(response, "html.parser")

    pre_div = soup.find("pre")

    pre_text_lines = pre_div.get_text().splitlines()

    for line in pre_text_lines:
        # Find attributes for the current line
        line_tag = pre_div.find(string=line)
        attributes = line_tag.parent.attrs if line_tag else {}

        # Write the text and attributes to the CSV file
        row = [line, attributes, "\n"]
        csvFile.write(str(row))

    # csvFile.write(pre_div.get_text())
