import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load nutrition data
with open("model/nutrition_data.json") as f:
    data = json.load(f)

# Function to calculate nutrients
def estimate(ingredients):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for item in ingredients:
        for key, val in data.items():
            if key in item.lower():
                amt = 1
                if "cup" in item:
                    amt = val.get("g_per_cup", 100) / 100
                if "tbsp" in item:
                    amt = val.get("g_per_tbsp", 15) / 100
                if "g" in item:
                    num = ''.join([c for c in item if c.isdigit()])
                    if num:
                        amt = float(num) / 100
                for k in total:
                    total[k] += val[k] * amt
    return total

# API endpoint
@app.route('/estimate', methods=['POST'])
def estimate_route():
    ing = request.json.get("ingredients", [])
    result = estimate(ing)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
