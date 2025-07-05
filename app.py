# app.py
from flask import Flask, render_template, json, request
import os

app = Flask(__name__)

# Path to your JSON forecast file
DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_forecast.json")


@app.route("/")
def dashboard():
    # Load the JSON data
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    city = data.get("city", {}).get("name", "Unknown")
    forecasts = data.get("list", [])

    # Pagination params
    page = request.args.get("page", 1, type=int)
    per_page = 5
    total = len(forecasts)
    total_pages = (total + per_page - 1) // per_page

    # Slice out the forecasts for this page
    start = (page - 1) * per_page
    end = start + per_page
    page_forecasts = forecasts[start:end]

    return render_template(
        "dashboard.html",
        city=city,
        forecasts=page_forecasts,
        page=page,
        total_pages=total_pages,
    )


if __name__ == "__main__":
    app.run(debug=True)
