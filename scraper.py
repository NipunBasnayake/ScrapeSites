import requests
from bs4 import BeautifulSoup
import csv, json, os
import pandas as pd
import time
import logging
from urllib.parse import urljoin

LOG_PATH = os.path.join("logs", "scraper.log")
os.makedirs("logs", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

DEFAULT_HEADERS = {"User-Agent": "IndustrialScraper/1.0 (+https://example.com)"}


def _save_outputs(data_list, base_name="scraped_data"):
    # ensure outputs dir
    csv_path = os.path.join("outputs", base_name + ".csv")
    json_path = os.path.join("outputs", base_name + ".json")
    xlsx_path = os.path.join("outputs", base_name + ".xlsx")

    # CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "value"])
        for i, v in enumerate(data_list, 1):
            writer.writerow([i, v])

    # JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    # Excel via pandas
    df = pd.DataFrame({"value": data_list})
    df.to_excel(xlsx_path, index_label="index")

    return {"csv": csv_path, "json": json_path, "xlsx": xlsx_path}


def scrape_data(
    url,
    selector_type="class",
    selector_value="",
    attr=None,
    pagination=None,  # dict: {"pattern": "https://site/page={}", "start":1, "count":5, "delay":1}
    timeout=10,
    headers=None,
):
    """
    Return (success:bool, payload: dict or error string)
    payload when success contains:
      { "data": [ ... ], "files": {csv/json/xlsx paths} }
    """
    headers = headers or DEFAULT_HEADERS
    results = []
    errors = []
    try:
        pages = 1
        page_urls = [url]

        # build pagination urls if requested
        if pagination:
            pattern = pagination.get("pattern")
            start = int(pagination.get("start", 1))
            count = int(pagination.get("count", 1))
            if pattern:
                page_urls = []
                for i in range(start, start + count):
                    page_urls.append(pattern.format(i))
                pages = len(page_urls)

        for idx, page_url in enumerate(page_urls, 1):
            try:
                resp = requests.get(page_url, timeout=timeout, headers=headers)
                resp.raise_for_status()
            except Exception as e:
                errors.append(f"Page fetch failed ({page_url}): {e}")
                logging.warning(errors[-1])
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # find elements by selector type
            if selector_type == "class":
                elements = soup.find_all(class_=selector_value)
            elif selector_type == "id":
                el = soup.find(id=selector_value)
                elements = [el] if el else []
            elif selector_type == "tag":
                elements = soup.find_all(selector_value)
            elif selector_type == "css":
                elements = soup.select(selector_value)
            else:
                return False, f"Unknown selector_type: {selector_type}"

            # extract attribute or text
            for el in elements:
                if attr:
                    val = el.get(attr)
                    # if attribute is URL-like, make absolute
                    if (
                        val
                        and isinstance(val, str)
                        and (val.startswith("/") or val.startswith("./"))
                    ):
                        try:
                            val = urljoin(page_url, val)
                        except Exception:
                            pass
                else:
                    val = el.get_text(" ", strip=True)
                if val:
                    results.append(val)

            # polite delay between pages (if pagination)
            if pagination and idx < pages:
                time.sleep(float(pagination.get("delay", 1)))

        if not results:
            msg = "No data found for that selector."
            logging.info(msg)
            return False, msg

        files = _save_outputs(results)
        return True, {"data": results, "files": files, "errors": errors}

    except Exception as e:
        logging.exception("Fatal scraper error")
        return False, str(e)
