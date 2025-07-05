from flask import Flask, render_template, json
import os

app = Flask(__name__)

# Path to your JSON forecast file
DATA_FILE = os.path.join(
    os.path.dirname(__file__), "forecast_columbus_us_20250705_135436.json"
)


@app.route("/")
def dashboard():
    # Load the JSON data
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    city = data.get("city", {}).get("name", "Unknown")
    forecasts = data.get("list", [])

    return render_template("dashboard.html", city=city, forecasts=forecasts)


if __name__ == "__main__":
    app.run(debug=True)
