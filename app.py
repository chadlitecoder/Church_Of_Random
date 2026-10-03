from flask import Flask, jsonify, render_template, request, send_from_directory
import requests

app = Flask(__name__)
RANDOM_ORG_URL = "https://www.random.org/integers/"


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/sounds/<path:filename>")
def sounds(filename):
    return send_from_directory("sounds", filename)


@app.get("/api/draw")
def draw():
    try:
        low = int(request.args.get("min", "0"))
        high = int(request.args.get("max", "1"))
    except ValueError:
        return jsonify(error="Choice range must be whole numbers."), 400
    if low < 0 or high < low or high - low > 99:
        return jsonify(error="Choose between 2 and 100 options."), 400

    params = {"num": 1, "min": low, "max": high, "col": 5,
              "base": 10, "format": "plain", "rnd": "new"}
    try:
        response = requests.get(RANDOM_ORG_URL, params=params, timeout=12)
        response.raise_for_status()
        body = response.text.strip()
        if body.startswith("Error:"):
            return jsonify(error=f"RANDOM.ORG: {body}"), 502
        result = int(body)
        if not low <= result <= high:
            raise ValueError("The random number was outside the requested range.")
        return jsonify(number=result)
    except requests.RequestException:
        return jsonify(error="RANDOM.ORG could not be reached. Please try again."), 502
    except ValueError:
        return jsonify(error="RANDOM.ORG returned an unreadable result. Please try again."), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
