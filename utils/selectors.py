import re
from bs4 import BeautifulSoup

def extract_value(el, attr=None, regex=None, page_url=None):
    from urllib.parse import urljoin

    if attr:
        val = el.get(attr)
        if val and (val.startswith("/") or val.startswith("./")):
            val = urljoin(page_url, val)
    else:
        val = el.get_text(" ", strip=True)

    if val and regex:
        match = re.search(regex, val)
        if match:
            val = match.group(1) if match.groups() else match.group(0)

    return val.strip() if val else None


def find_elements(soup, selector_type, selector_value):
    if selector_type == "class":
        return soup.find_all(class_=selector_value)
    elif selector_type == "id":
        el = soup.find(id=selector_value)
        return [el] if el else []
    elif selector_type == "tag":
        return soup.find_all(selector_value)
    elif selector_type == "css":
        return soup.select(selector_value)
    else:
        return []
