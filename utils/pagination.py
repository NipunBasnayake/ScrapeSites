from urllib.parse import urljoin

def detect_next_page(soup, base_url):
    next_link = soup.find("a", string=lambda s: s and "next" in s.lower())
    if next_link and next_link.get("href"):
        return urljoin(base_url, next_link["href"])
    return None
