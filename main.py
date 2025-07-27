import tkinter as tk
from tkinter import messagebox
import subprocess
import platform
from scraper import scrape_div_class

def on_scrape_click():
    url = url_entry.get().strip()
    div_class = div_class_entry.get().strip()
    if not url or not div_class:
        messagebox.showerror("Input Error", "Please enter both URL and Div class name.")
        return

    success, message = scrape_div_class(url, div_class)
    if success:
        messagebox.showinfo("Success", "✅ " + message)
    else:
        messagebox.showwarning("Warning", message)

def open_csv():
    try:
        filename = "scraped_data.csv"
        if platform.system() == "Windows":
            subprocess.run(["start", filename], shell=True)
        elif platform.system() == "Darwin":
            subprocess.run(["open", filename])
        else:
            subprocess.run(["xdg-open", filename])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file:\n{e}")

window = tk.Tk()
window.title("Div Class Scraper")

window_width = 500
window_height = 280
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)
window.configure(bg="#f4f4f4")

label_font = ("Segoe UI", 12)
entry_font = ("Segoe UI", 11)
button_font = ("Segoe UI", 11, "bold")

frame = tk.Frame(window, bg="#f4f4f4", padx=20, pady=20)
frame.pack(expand=True)

heading = tk.Label(frame, text="Scrape Text by Div Class Name", font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333")
heading.pack(pady=(0, 15))

url_label = tk.Label(frame, text="Enter Website URL:", font=label_font, bg="#f4f4f4", anchor="w")
url_label.pack(fill='x')
url_entry = tk.Entry(frame, width=50, font=entry_font, relief="groove", borderwidth=2)
url_entry.pack(pady=(2, 12))

div_class_label = tk.Label(frame, text="Enter Div Class Name:", font=label_font, bg="#f4f4f4", anchor="w")
div_class_label.pack(fill='x')
div_class_entry = tk.Entry(frame, width=50, font=entry_font, relief="groove", borderwidth=2)
div_class_entry.pack(pady=(2, 15))

btn_frame = tk.Frame(frame, bg="#f4f4f4")
btn_frame.pack()

scrape_btn = tk.Button(
    btn_frame,
    text="Scrape Data",
    font=button_font,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="flat",
    padx=15,
    pady=7,
    command=on_scrape_click
)
scrape_btn.grid(row=0, column=0, padx=10)

open_btn = tk.Button(
    btn_frame,
    text="Open CSV",
    font=button_font,
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    relief="flat",
    padx=15,
    pady=7,
    command=open_csv
)
open_btn.grid(row=0, column=1, padx=10)

window.mainloop()
