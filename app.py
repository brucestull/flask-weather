# app.py
from flask import Flask, render_template, json, request, url_for
import os
from collections import OrderedDict
from datetime import datetime

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "sample_forecast.json")


def group_by_day(raw_list):
    days = OrderedDict()
    for fc in raw_list:
        date_str = fc["dt_txt"].split(" ")[0]
        days.setdefault(date_str, []).append(fc)
    return days


def pick_period_entry(entries, start_hour, end_hour):
    """
    From a list of forecast entries, pick the one whose time is
    in [start_hour, end_hour). If multiple, pick the one nearest
    the midpoint of that interval; otherwise return None.
    """
    bucket = []
    for fc in entries:
        dt = datetime.strptime(fc["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if start_hour <= dt.hour < end_hour:
            bucket.append(
                (abs((dt.hour + dt.minute / 60) - ((start_hour + end_hour) / 2)), fc)
            )
    if not bucket:
        return None
    # pick entry with minimal distance to period midpoint
    _, chosen = min(bucket, key=lambda x: x[0])
    return chosen


@app.route("/")
def dashboard():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    city = data.get("city", {}).get("name", "Unknown")
    raw = data.get("list", [])

    # group and paginate by day
    days = group_by_day(raw)
    dates = list(days.keys())
    total_pages = len(dates)
    page = request.args.get("page", 1, type=int)
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


@app.route("/summary")
def summary():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    city = data.get("city", {}).get("name", "Unknown")
    raw = data.get("list", [])

    # group by day, then take the first 7 days
    days = group_by_day(raw)
    first7 = list(days.items())[:7]

    summary = []
    for date_str, entries in first7:
        morning = pick_period_entry(entries, 6, 12)
        midday = pick_period_entry(entries, 12, 18)
        evening = pick_period_entry(entries, 18, 24)
        summary.append(
            {
                "date": date_str,
                "morning": morning,
                "midday": midday,
                "evening": evening,
            }
        )

    return render_template("summary.html", city=city, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
