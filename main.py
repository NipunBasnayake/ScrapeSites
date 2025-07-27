import tkinter as tk
from tkinter import messagebox
from scraper import scrape_paragraphs

def on_scrape_click():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Input Error", "Please enter a valid URL.")
        return

    success, message = scrape_paragraphs(url)
    if success:
        messagebox.showinfo("Success! " + message)
    else:
        messagebox.showwarning("Warning", message)


window = tk.Tk()
window.title("Website Paragraph Scraper")

window_width = 450
window_height = 220
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

heading = tk.Label(frame, text="Enter Website URL to Scraper", font=("Segoe UI", 14, "bold"), bg="#f4f4f4", fg="#333")
heading.pack(pady=(0, 10))

url_entry = tk.Entry(frame, width=45, font=entry_font, relief="groove", borderwidth=2)
url_entry.pack(pady=(2, 10))

scrape_btn = tk.Button(
    frame,
    text="Scrape Data",
    font=button_font,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="flat",
    padx=10,
    pady=5,
    command=on_scrape_click
)
scrape_btn.pack(pady=10)

window.mainloop()
