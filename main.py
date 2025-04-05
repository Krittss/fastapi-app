from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import uvicorn
from typing import List

app = FastAPI()

# Mount static files
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
#templates = Jinja2Templates(directory="templates")

# Load the trained model (if needed for prediction)
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("Warning: Model file not found!")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 Serve Frontend Pages
@app.get("/")
def home():
    return {"message": "Welcome to the API"}

@app.get("/login")
def login_page():
    return {"message": "Login Page"}

@app.get("/signup")
def signup_page():
    return {"message": "Signup Page"}

# 👉 API Endpoint for Prediction (if needed)
class InputData(BaseModel):
    data: list

feature_names = [
    'Age',
    'Number of sexual partners',
    'First sexual intercourse',
    'Num of pregnancies',
    'Smokes',
    'Hormonal Contraceptives',
    'STDs',
    'STDs: Number of diagnosis',
    'STDs: Time since last diagnosis',
    'STDs: Time since first diagnosis'
]
@app.post("/predict")
def predict(data: List[float]):
    print(f"Received Input: data={data}")
    
    # Convert list to DataFrame with column names
    input_df = pd.DataFrame([data], columns=feature_names)

    # Make prediction
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df).max() * 100  # confidence %

    return {
        "prediction": int(prediction[0]),
        "confidence": f"{probability:.2f}%"
    }
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run the FastAPI app using: uvicorn main:app --reload
