import requests
from bs4 import BeautifulSoup
import csv

def scrape_paragraphs(url, output_file="scraped_data.csv"):
    """
    Scrape all <p> tag texts from the URL and save to a CSV file.
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        for para in soup.find_all("p"):
            text = para.get_text(strip=True)
            if text:
                data.append([text])

        if data:
            with open(output_file, mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Paragraph Text"])
                writer.writerows(data)
            return True, f"Data scraped and saved as '{output_file}'"
        else:
            return False, "No <p> tags found on this page."
    except Exception as e:
        return False, f"An error occurred: {e}"
