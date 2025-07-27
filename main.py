import requests
from bs4 import BeautifulSoup
import csv

# Fetch page
url = "https://www.python.org/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract upcoming events
data = []
events_section = soup.find("div", class_="medium-widget event-widget last")

if events_section:
    for li in events_section.find_all("li"):
        title = li.find("a").get_text(strip=True)
        link = "https://www.python.org" + li.find("a")["href"]
        date = li.find("time").get_text(strip=True)
        data.append([title, date, link])

# Save to CSV
with open("python_org_events.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Event Title", "Date", "Link"])
    writer.writerows(data)

print("Event report saved as 'python_org_events.csv'")
