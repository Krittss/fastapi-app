from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import pickle
import sqlite3
import os

# Initialize FastAPI app
app = FastAPI()

# Load ML Model
MODEL_PATH = "model.pkl"
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    model = None

# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database connection
DB_PATH = "predictions.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

# Create a table for storing predictions
conn, cursor = get_db()
cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER, 
    partners INTEGER, 
    first_intercourse INTEGER,
    pregnancies INTEGER,
    smokes INTEGER,
    stds INTEGER,
    stds_hpv INTEGER,
    stds_hiv INTEGER,
    dx_cancer INTEGER,
    dx INTEGER,
    result TEXT
)''')
conn.commit()
conn.close()

# Home Route - Displays Form
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("s1.html", {"request": request})

# Predict Route
@app.post("/predict")
async def predict(
    request: Request,
    age: int = Form(...),
    partners: int = Form(...),
    first_intercourse: int = Form(...),
    pregnancies: int = Form(...),
    smokes: int = Form(...),
    stds: int = Form(...),
    stds_hpv: int = Form(...),
    stds_hiv: int = Form(...),
    dx_cancer: int = Form(...),
    dx: int = Form(...)
):
    if model is None:
        return {"error": "Model not found"}

    input_data = pd.DataFrame([{
        "Age": age,
        "Number of sexual partners": partners,
        "First sexual intercourse": first_intercourse,
        "Num of pregnancies": pregnancies,
        "Smokes": smokes,
        "STDs": stds,
        "STDs:HPV": stds_hpv,
        "STDs:HIV": stds_hiv,
        "Dx:Cancer": dx_cancer,
        "Dx": dx
    }])

    prediction = model.predict(input_data)[0]

    # Save prediction to database
    conn, cursor = get_db()
    cursor.execute(
        '''INSERT INTO predictions (age, partners, first_intercourse, pregnancies, smokes, stds, stds_hpv, stds_hiv, dx_cancer, dx, result) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (age, partners, first_intercourse, pregnancies, smokes, stds, stds_hpv, stds_hiv, dx_cancer, dx, prediction)
    )
    conn.commit()
    conn.close()

    return templates.TemplateResponse("result.html", {"request": request, "result": prediction})
