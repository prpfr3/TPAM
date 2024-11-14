"""
Extracts Railway Acts from the UK Government Legislation site
"""

import requests, csv, os
from bs4 import BeautifulSoup

output_file = os.path.join("D:\\Data", "TPAM", "Companies_Extract_AoP3.csv")

with open(output_file, "wt+", newline="", encoding="utf-8") as csvFile:
    output = csv.writer(csvFile)
    csvrow = ["title", "title_url", "reference", "reference_url", "type"]
    output.writerow(csvrow)
    count = 0

    # for i in range(1802, 2024):
    for i in range(1, 251):
        url = f"https://www.legislation.gov.uk/primary+secondary?title=railway&page={i}"
        # url = f"https://www.legislation.gov.uk/primary+secondary/{i}?title=railway"

        try:
            res = requests.get(url).content.decode("utf-8", "ignore")

        except requests.exceptions.ConnectionError as err:
            # eg, no internet
            raise SystemExit(err) from err
        except requests.exceptions.HTTPError as err:
            # eg, url, server and other errors
            raise SystemExit(err) from err

        soup = BeautifulSoup(res, "html.parser")

        tables = soup.find_all("table")

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

                if csv_output_row:
                    output.writerow(csv_output_row)
                    count = count + 1

        print(f"Retrieved page {i} and rows now {count}")
