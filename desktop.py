import threading
import webview
from app import app

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    webview.create_window(
        "Industrial Web Scraper",
        "http://127.0.0.1:5000",
        width=1200,
        height=800,
        resizable=True
    )
    webview.start()
