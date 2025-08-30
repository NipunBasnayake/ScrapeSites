import os, csv, json, time, logging, requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils.selectors import extract_value, find_elements
from utils.pagination import detect_next_page
from utils.request_handler import get

LOG_PATH = os.path.join("logs", "scraper.log")
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

DEFAULT_HEADERS = {"User-Agent": "IndustrialScraper/2.0 (+https://example.com)"}

def _save_outputs(data_list, base_name="scraped_data"):
    csv_path = os.path.join("outputs", base_name + ".csv")
    json_path = os.path.join("outputs", base_name + ".json")
    xlsx_path = os.path.join("outputs", base_name + ".xlsx")

    # CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
        writer.writeheader()
        writer.writerows(data_list)

    # JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    # Excel
    pd.DataFrame(data_list).to_excel(xlsx_path, index=False)

    return {"csv": csv_path, "json": json_path, "xlsx": xlsx_path}

def scrape_data(
    url,
    selectors=[{"type": "class", "value": "title", "attr": None, "regex": None}],
    nested_selectors=None,
    pagination_auto=False,
    timeout=10,
    headers=None,
):
    headers = headers or DEFAULT_HEADERS
    results = []
    errors = []

    def scrape_page(page_url, timeout, headers):
        resp = get(page_url, timeout=timeout, headers=headers)
        if not resp:
            errors.append(f"Failed to fetch {page_url}")
            return None
        return BeautifulSoup(resp.text, "html.parser")

    page_url = url
    while page_url:
        soup = scrape_page(page_url)
        if not soup:
            break

        # extract data
        rows = []
        for i, sel in enumerate(selectors):
            elements = find_elements(soup, sel["type"], sel["value"])
            if not rows:
                rows = [{} for _ in range(len(elements))]
            for idx, el in enumerate(elements):
                rows[idx][f"field_{i+1}"] = extract_value(el, sel.get("attr"), sel.get("regex"), page_url)

        # nested scraping
        if nested_selectors:
            for row in rows:
                link = row.get("field_1")
                if link:
                    nested_soup = scrape_page(link)
                    if nested_soup:
                        for j, sel in enumerate(nested_selectors):
                            els = find_elements(nested_soup, sel["type"], sel["value"])
                            row[f"nested_{j+1}"] = extract_value(
                                els[0], sel.get("attr"), sel.get("regex"), link
                            ) if els else None

        results.extend(rows)

        # pagination
        if pagination_auto:
            next_page = detect_next_page(soup, page_url)
            if next_page:
                page_url = next_page
                time.sleep(1)
            else:
                break
        else:
            break

    if not results:
        return False, "No data found."

    files = _save_outputs(results)
    return True, {"data": results, "files": files, "errors": errors}
