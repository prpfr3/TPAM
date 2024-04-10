# -*- coding: utf-8 -*-
"""
Scrape a table from wikipedia using python. Allows for cells spanning multiple rows and/or columns. Outputs csv files for
each table
url: https://gist.github.com/wassname/5b10774dfcd61cdd3f28
authors: panford, wassname, muzzled, Yossi
license: MIT
"""

from bs4 import BeautifulSoup
import requests
import os
import codecs

urls = ["https://en.wikipedia.org/wiki/Locomotives_of_the_Furness_Railway"]

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
filename = os.path.join(DATAIO_DIR, "Class_FR_Extract.csv")

for url in urls:
    header = {"User-Agent": "Mozilla/5.0"}  # Needed to prevent 403 error on Wikipedia
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content)

    tables = soup.findAll("table", {"class": "wikitable"})

    f = codecs.open(filename, "w", encoding="utf-8")
    # show tables
    for i, table in enumerate(tables):
        print("#" * 10 + f"Table {i}" + "#" * 10)
        print(table.text[:100])
        print("." * 80)
    print("#" * 80)

    for tn, table in enumerate(tables):
        # preinit list of lists
        rows = table.findAll("tr")
        row_lengths = [len(r.findAll(["th", "td"])) for r in rows]
        ncols = max(row_lengths)
        nrows = len(rows)
        data = []

        for i in range(nrows):
            rowD = []
            for j in range(ncols):
                rowD.append("")
            data.append(rowD)

        attributes = []
        for i in range(nrows):
            rowA = []
            for j in range(ncols):
                rowA.append("")
            attributes.append(rowA)

        images = []
        for i in range(nrows):
            rowI = []
            for j in range(ncols):
                rowI.append("")
            images.append(rowI)

        # process html
        for i in range(len(rows)):
            row = rows[i]
            cells = row.findAll(["td", "th"])
            for j in range(len(cells)):
                cell = cells[j]

                # lots of cells span cols and rows so lets deal with that
                cspan = int(cell.get("colspan", 1))
                rspan = int(cell.get("rowspan", 1))
                l = 0
                for k in range(rspan):
                    # Shifts to the first empty cell of this row
                    while data[i + k][j + l]:
                        l += 1
                    for m in range(cspan):
                        cell_n = j + l + m
                        row_n = i + k
                        # in some cases the colspan can overflow the table, in those cases just get the last item
                        cell_n = min(cell_n, len(data[row_n]) - 1)
                        data[row_n][cell_n] += cell.text
                        if a := cell.find("a", href=True):
                            images[row_n][cell_n] = a["href"]
                        if img := cell.find("img"):
                            images[row_n][cell_n] = img["src"]

        for i in range(nrows):
            rowStr1 = "\t".join(data[i])
            rowStr1 = rowStr1.replace("\n", "")
            print(f"{rowStr1=}")

            rowStr2 = "\t".join(attributes[i])
            rowStr2 = rowStr2.replace("\n", "")
            print(f"{rowStr2=}")

            rowStr3 = "\t".join(images[i])
            rowStr3 = rowStr3.replace("\n", "")
            print(f"{rowStr3=}")

            rowStr = rowStr1 + "\t" + rowStr2 + "\t" + rowStr3
            print(f"{rowStr=}")

            f.write(rowStr + "\n")

    f.close()
