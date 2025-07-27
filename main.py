import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox

def scrape_data():
    url = entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        for para in soup.find_all("p"):
            text = para.get_text(strip=True)
            if text:
                data.append([text])

        if data:
            with open("scraped_data.csv", mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Paragraph Text"])
                writer.writerows(data)
            messagebox.showinfo("Success", "Data scraped and saved to 'scraped_data.csv'")
        else:
            messagebox.showinfo("No Data", "No paragraph data found on the page.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# GUI Setup
window = tk.Tk()
window.title("Website Paragraph Scraper")
window.geometry("400x180")

tk.Label(window, text="Enter Website URL:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(window, width=50)
entry.pack(pady=5)

scrape_btn = tk.Button(window, text="Scrape Data", command=scrape_data, bg="green", fg="white", font=("Arial", 11))
scrape_btn.pack(pady=15)

window.mainloop()
