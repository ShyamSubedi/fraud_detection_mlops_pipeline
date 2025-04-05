import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://ekaakkjobkspuuolpzgz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVrYWFra2pvYmtzcHV1b2xwemd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2MDcxNDUsImV4cCI6MjA1OTE4MzE0NX0.XSvD9u97sVUq6szoTtTR40lR2YrfKtZtct6BZbqUZfM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# API URL
API_URL = "http://a88c4be839c614e3aa350f31a246ffa8-873650023.us-east-2.elb.amazonaws.com/predict"


st.set_page_config(page_title="Fraud Detection Dashboard", layout="centered")
st.title("💳 Real-Time Fraud Detection")

with st.form("fraud_form"):
    st.subheader("Enter Transaction Details")
    step = st.number_input("Step", min_value=1, value=1)
    amount = st.number_input("Amount", min_value=0.0, value=1000.0)
    oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0, value=5000.0)
    newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0, value=4000.0)
    oldbalanceDest = st.number_input("Old Balance (Dest)", min_value=0.0, value=0.0)
    newbalanceDest = st.number_input("New Balance (Dest)", min_value=0.0, value=1000.0)
    isFlaggedFraud = st.selectbox("Is Flagged Fraud", [0, 1])

    st.markdown("**Transaction Type (One-Hot):**")
    type_CASH_IN = st.checkbox("CASH_IN")
    type_CASH_OUT = st.checkbox("CASH_OUT")
    type_DEBIT = st.checkbox("DEBIT")
    type_PAYMENT = st.checkbox("PAYMENT")
    type_TRANSFER = st.checkbox("TRANSFER")

    submitted = st.form_submit_button("Predict")

if submitted:
    input_data = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "isFlaggedFraud": isFlaggedFraud,
        "type_CASH_IN": int(type_CASH_IN),
        "type_CASH_OUT": int(type_CASH_OUT),
        "type_DEBIT": int(type_DEBIT),
        "type_PAYMENT": int(type_PAYMENT),
        "type_TRANSFER": int(type_TRANSFER)
    }

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()
            if "error" in result:
                st.error("Prediction failed: " + result["error"])
            else:
                st.success(f"🚨 Fraud: {bool(result['prediction'])}")
                st.write(f"Fraud Probability: **{result['fraud_probability']}**")
        except Exception as e:
            st.error(f"API error: {e}")

st.markdown("---")
st.subheader("📜 Recent Predictions (Logs)")

try:
    logs = supabase.table("logs").select("*").order("timestamp", desc=True).limit(10).execute()
    log_data = pd.DataFrame(logs.data)
    if not log_data.empty:
        log_data["timestamp"] = pd.to_datetime(log_data["timestamp"])
        log_data = log_data[["timestamp", "prediction", "fraud_probability", "features"]]
        st.dataframe(log_data)
    else:
        st.info("No logs available yet.")
except Exception as e:
    st.error(f"Failed to fetch logs: {e}")
