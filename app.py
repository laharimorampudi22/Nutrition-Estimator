from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Mount folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ✅ Simple mock nutrition database
NUTRITION_DB = {
    "rice": {"kcal": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
    "oil": {"kcal": 884, "protein": 0, "fat": 100, "carbs": 0},
    "chicken": {"kcal": 239, "protein": 27, "fat": 14, "carbs": 0},
    "milk": {"kcal": 42, "protein": 3.4, "fat": 1, "carbs": 5},
    "egg": {"kcal": 155, "protein": 13, "fat": 11, "carbs": 1.1}
}

# ✅ Function to estimate totals
def estimate_nutrition(ingredients: str):
    total = {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0}
    for item in ingredients.split(","):
        words = item.strip().lower().split()
        for food, vals in NUTRITION_DB.items():
            if food in words:
                for k in total:
                    total[k] += vals[k]
    return total

# ✅ Route for homepage
@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Route for prediction
@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, ingredients: str = Form(...)):
    result = estimate_nutrition(ingredients)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "ingredients": ingredients}
    )
