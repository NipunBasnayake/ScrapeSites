import requests
from bs4 import BeautifulSoup
import csv

# Fetch page
url = "https://threejs.org/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all <h2> tags
data = []
for heading in soup.find_all("h2"):
    text = heading.get_text(strip=True)
    data.append([text])

# Save to CSV
with open("headings_report.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Heading"])
    writer.writerows(data)

print("Report saved as 'headings_report.csv'")
