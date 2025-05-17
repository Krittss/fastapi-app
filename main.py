from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import numpy as np
import uvicorn

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

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

@app.post("/predict")
def predict(input_data: InputData):
    print("Received Input:", input_data)  # Debugging Line
    
    if model is None:
        return {"error": "Model not loaded"}

    # Convert list to NumPy array
    input_array = np.array(input_data.data).reshape(1, -1)
    
    # Run the prediction
    prediction = model.predict(input_array)[0]
    
    return {"prediction": "Positive" if prediction == 1 else "Negative"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run the FastAPI app using: uvicorn main:app --reload
