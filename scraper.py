import requests
from bs4 import BeautifulSoup
import csv

def scrape_div_class(url, div_class, output_file="scraped_data.csv"):
    """
    Scrape all text inside <div class="{div_class}"> from the URL and save to CSV.
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        divs = soup.find_all("div", class_=div_class)
        if not divs:
            return False, f"No <div class='{div_class}'> elements found."

        data = []
        for div in divs:
            text = div.get_text(separator=" ", strip=True)
            if text:
                data.append([text])

        if data:
            with open(output_file, mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([f"Text inside div class '{div_class}'"])
                writer.writerows(data)
            return True, f"Data scraped and saved as '{output_file}'"
        else:
            return False, f"No text found inside <div class='{div_class}'> elements."
    except Exception as e:
        return False, f"An error occurred: {e}"
