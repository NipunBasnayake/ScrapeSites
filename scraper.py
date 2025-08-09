import requests
from bs4 import BeautifulSoup
import csv

def scrape_div_class(url, div_class):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        divs = soup.find_all("div", class_=div_class)
        data = [div.get_text(strip=True) for div in divs]

        if not data:
            return False, "No data found for that class."

        with open("scraped_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Scraped Data"])
            for item in data:
                writer.writerow([item])

        return True, data
    except Exception as e:
        return False, str(e)
