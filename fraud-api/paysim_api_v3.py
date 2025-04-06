from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Added CORS
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize app
app = FastAPI(title="PaySim Fraud Detection API")

# ✅ Enable CORS to prevent 403 errors from external requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input schema
class Transaction(BaseModel):
    step: int
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    isFlaggedFraud: int
    type_CASH_IN: int
    type_CASH_OUT: int
    type_DEBIT: int
    type_PAYMENT: int
    type_TRANSFER: int

# Load the trained model
model = joblib.load("data/paysim_xgb_model_final.pkl")

# Define the prediction endpoint
@app.post("/predict")
def predict(transaction: Transaction):
    features = np.array([[
        transaction.step,
        transaction.amount,
        transaction.oldbalanceOrg,
        transaction.newbalanceOrig,
        transaction.oldbalanceDest,
        transaction.newbalanceDest,
        transaction.isFlaggedFraud,
        transaction.type_CASH_IN,
        transaction.type_CASH_OUT,
        transaction.type_DEBIT,
        transaction.type_PAYMENT,
        transaction.type_TRANSFER
    ]])
    
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {"prediction": int(prediction), "fraud_probability": round(probability, 4)}
