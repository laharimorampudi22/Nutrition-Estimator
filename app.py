from flask import Flask, render_template, request, jsonify
import json, re

app = Flask(__name__)

# Load simple nutrition database
with open('model/nutrition_data.json') as f:
    NUTRITION_DATA = json.load(f)

def estimate_nutrition(ingredients_text):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}

    # Split ingredients by comma
    ingredients = [i.strip() for i in ingredients_text.split(",")]

    for ing in ingredients:
        match = re.search(r"([0-9.]+)\\s*(cup|tbsp|tsp|g|gram|grams)?\\s*(.*)", ing)
        if not match:
            continue
        qty = float(match.group(1))
        unit = match.group(2) or "unit"
        name = match.group(3).strip().lower()

        for key in NUTRITION_DATA:
            if key in name:
                data = NUTRITION_DATA[key]
                # scale by quantity
                scale = qty
                if "cup" in unit: scale *= data.get("g_per_cup", 100) / 100
                elif "tbsp" in unit: scale *= data.get("g_per_tbsp", 15) / 100
                elif "g" in unit: scale *= 1 / 100

                for k in total:
                    total[k] += data[k] * scale

    return {k: round(v, 2) for k, v in total.items()}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/estimate", methods=["POST"])
def estimate():
    text = request.form["ingredients"]
    result = estimate_nutrition(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
