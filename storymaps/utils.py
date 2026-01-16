import time
import requests_cache
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Enable polite caching (7 days)
requests_cache.install_cache(
    "wiki_cache",
    expire_after=60 * 60 * 24 * 7,
    allowable_methods=("GET",),
)

def get_wikipedia_summary(url, delay=1.0):
    """
    Fetch and cache the summary paragraph from a Wikipedia page.
    Returns a fallback message if not available.
    """

    headers = {
        "User-Agent": "TPAM Django Project (https://github.com/prpfr3; contact@example.com)"
    }

    session = requests_cache.CachedSession()

    # Check if URL is cached
    cached = session.cache.contains(url)
    if not cached:
        print(f"⌛ Waiting {delay:.1f}s before new request to {url} ...")
        time.sleep(delay)

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return "No further information available from TPAM or Wikipedia"

    if getattr(response, "from_cache", False):
        print(f"ℹ️ Loaded from cache: {url}")
    else:
        print(f"⬇️ Downloaded: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main article content
    body_content_div = soup.find("div", id="bodyContent")
    if not body_content_div:
        print(f"⚠️ bodyContent div not found in {url}")
        return "No further information available from TPAM or Wikipedia"

    # Extract the first meaningful <p> paragraph from the content
    paragraphs = body_content_div.find_all("p")
    summary_text = ""
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text:
            summary_text = p.decode_contents()  # keep inline formatting, links, etc.
            break

    if not summary_text:
        return "No further information available from TPAM or Wikipedia"

    # Clean and fix internal links
    summary_text = summary_text.replace('href="/wiki/', 'href="https://en.wikipedia.org/wiki/')

    return f"<p>From Wikipedia:</p>{summary_text}"
