import requests


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
