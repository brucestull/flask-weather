# app.py
from flask import Flask, render_template, json, request, url_for
import os
from collections import OrderedDict
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_forecast.json")


@app.route("/")
def dashboard():
    # load raw list
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    city = data.get("city", {}).get("name", "Unknown")
    raw = data.get("list", [])

    # group by date (YYYY-MM-DD)
    days = OrderedDict()
    for fc in raw:
        date_str = fc["dt_txt"].split(" ")[0]
        days.setdefault(date_str, []).append(fc)

    # pagination on days
    dates = list(days.keys())
    total_pages = len(dates)
    page = request.args.get("page", 1, type=int)
    # clamp page
    page = max(1, min(page, total_pages))

    selected_date = dates[page - 1]
    day_forecasts = days[selected_date]

    return render_template(
        "dashboard.html",
        city=city,
        date=selected_date,
        forecasts=day_forecasts,
        page=page,
        total_pages=total_pages,
        dates=dates,
    )


if __name__ == "__main__":
    app.run(debug=True)
