import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import threading
import re
from scraper import scrape_div_class

def validate_url(url):
    pattern = re.compile(r'^(http|https)://')
    return bool(pattern.match(url))

def run_scraper():
    url = url_entry.get().strip()
    div_class = div_class_entry.get().strip()

    if not url or not div_class:
        messagebox.showerror("Input Error", "Please enter both URL and Div class name.")
        return
    
    if not validate_url(url):
        messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http:// or https://")
        return

    progress.start()
    status_var.set("Scraping in progress...")
    scrape_btn.config(state="disabled")

    def scrape_task():
        try:
            success, message = scrape_div_class(url, div_class)
            if success:
                status_var.set("✅ Scraping completed successfully")
                messagebox.showinfo("Success", message)
                if auto_open_var.get():
                    open_csv()
            else:
                status_var.set("⚠ Warning during scraping")
                messagebox.showwarning("Warning", message)
        except Exception as e:
            status_var.set("❌ Error occurred")
            messagebox.showerror("Error", f"Scraping failed:\n{e}")
        finally:
            progress.stop()
            scrape_btn.config(state="normal")

    threading.Thread(target=scrape_task, daemon=True).start()

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
window.title("Industrial Web Scraper")
window.geometry("520x350")
window.resizable(False, False)

style = ttk.Style(window)
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
style.configure("TEntry", font=("Segoe UI", 11))

main_frame = ttk.Frame(window, padding=20)
main_frame.pack(fill="both", expand=True)

heading = ttk.Label(main_frame, text="🌐 Industrial Web Scraper", font=("Segoe UI", 16, "bold"))
heading.pack(pady=(0, 15))

ttk.Label(main_frame, text="Enter Website URL:").pack(anchor="w")
url_entry = ttk.Entry(main_frame, width=50)
url_entry.pack(pady=(0, 12))

ttk.Label(main_frame, text="Enter Div Class Name:").pack(anchor="w")
div_class_entry = ttk.Entry(main_frame, width=50)
div_class_entry.pack(pady=(0, 15))

auto_open_var = tk.BooleanVar(value=True)
ttk.Checkbutton(main_frame, text="Auto-open CSV after scraping", variable=auto_open_var).pack(anchor="w", pady=(0, 15))

btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=(0, 10))

scrape_btn = ttk.Button(btn_frame, text="🚀 Scrape Data", command=run_scraper)
scrape_btn.grid(row=0, column=0, padx=8)

open_btn = ttk.Button(btn_frame, text="📂 Open CSV", command=open_csv)
open_btn.grid(row=0, column=1, padx=8)

progress = ttk.Progressbar(main_frame, mode="indeterminate", length=400)
progress.pack(pady=(10, 5))

status_var = tk.StringVar(value="Ready")
status_label = ttk.Label(main_frame, textvariable=status_var, foreground="gray")
status_label.pack(anchor="w")

window.mainloop()
