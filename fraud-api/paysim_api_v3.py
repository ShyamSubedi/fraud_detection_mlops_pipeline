from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from datetime import datetime, timezone
from supabase import create_client, Client
import traceback
import sys

# ✅ Load model (relative path inside Docker container)
model = joblib.load("data/paysim_xgb_model_final.pkl")

# ✅ Supabase credentials
SUPABASE_URL = "https://ekaakkjobkspuuolpzgz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrYWFra2pvYmtzcHV1b2xwemd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2MDcxNDUsImV4cCI6MjA1OTE4MzE0NX0.XSvD9u97sVUq6szoTtTR40lR2YrfKtZtct6BZbqUZfM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ FastAPI app
app = FastAPI(title="PaySim Fraud Detection API")

# ✅ Input schema
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

# ✅ Prediction route
@app.post("/predict")
def predict(transaction: Transaction):
    try:
        features = {
            "step": transaction.step,
            "amount": transaction.amount,
            "oldbalanceOrg": transaction.oldbalanceOrg,
            "newbalanceOrig": transaction.newbalanceOrig,
            "oldbalanceDest": transaction.oldbalanceDest,
            "newbalanceDest": transaction.newbalanceDest,
            "isFlaggedFraud": transaction.isFlaggedFraud,
            "type_CASH_IN": transaction.type_CASH_IN,
            "type_CASH_OUT": transaction.type_CASH_OUT,
            "type_DEBIT": transaction.type_DEBIT,
            "type_PAYMENT": transaction.type_PAYMENT,
            "type_TRANSFER": transaction.type_TRANSFER
        }

        X = np.array([list(features.values())])
        probability = float(model.predict_proba(X)[0][1])
        prediction = int(probability > 0.5)

        # ✅ Log to Supabase
        log_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "features": features,
            "prediction": prediction,
            "fraud_probability": round(probability, 6)
        }

        response = supabase.table("logs").insert(log_payload).execute()
        print("✅ Supabase response:", response)

        return {
            "prediction": prediction,
            "fraud_probability": round(probability, 6)
        }

    except Exception:
        error_msg = traceback.format_exc()
        print("❌ Error during prediction or logging:\n", error_msg, file=sys.stderr)
        return {"error": "Prediction failed. Check server logs."}

# Trigger GitHub Actions – test commit
