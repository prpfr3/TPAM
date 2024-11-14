import requests
from bs4 import BeautifulSoup


def get_wikipage_html(url):
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the <div> tag with id=bodyContent
    body_content_div = soup.find("div", id="bodyContent")

    if body_content_div:

        # Remove mw-editsection and its descendants
        for element in body_content_div.select(".mw-editsection"):
            element.decompose()

        # Remove mw-editsection and its descendants
        for element in body_content_div.select(".box-More_citations_needed"):
            element.decompose()

        # Split the HTML content within the bodyContent div at the point where <div class="navbox-styles"> occurs
        split_html = str(body_content_div).split('<div class="navbox-styles">')

        # Keep only the first part of the split, which contains the content before navbox-styles
        html_within_body_content = (
            split_html[0]
            .replace("<span>edit<span>", "")
            .replace("/wiki/", "https://en.wikipedia.org/wiki/")
        )

        return html_within_body_content
    else:
        print("No <div> tag with id=bodyContent found.")
        return None


def get_wikipedia_page_content(title):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        "disabletoc": True,
    }

    headers = {"User-Agent": "TPAM Django Project @ https://github.com/prpfr3"}

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    if "parse" in data and "text" in data["parse"]:
        return data["parse"]["text"]["*"]
    else:
        return None


def save_content_to_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    page_title = "Elham_Valley_Railway"
    page_content = get_wikipedia_page_content(page_title)

    if page_content:
        file_path = f"{page_title}.html"
        save_content_to_file(file_path, page_content)
        print(f"Successfully saved the Wikipedia page to: {file_path}")
    else:
        print(f"Failed to retrieve the Wikipedia page: {page_title}")
