from flask import Flask, render_template, request, send_file
from scraper import scrape_div_class

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    message = None
    if request.method == "POST":
        url = request.form.get("url").strip()
        div_class = request.form.get("div_class").strip()
        success, result = scrape_div_class(url, div_class)
        if success:
            data = result
            message = "Scraping successful ✅"
        else:
            message = f"Error: {result}"
    return render_template("index.html", data=data, message=message)

@app.route("/download")
def download_csv():
    return send_file("scraped_data.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
