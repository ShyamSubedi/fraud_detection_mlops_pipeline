# Fraud Detection MLOps Pipeline

## Overview
This project demonstrates a full end-to-end MLOps pipeline for a real-time fraud detection system using synthetic financial transaction data (PaySim). It combines powerful tools and cloud-native technologies to simulate a production-grade setup.

---

## Goal
To create a scalable, real-time fraud detection system that:
- Ingests streaming data
- Makes live predictions
- Logs outcomes to a cloud database
- logs results in a live dashboard

---

## Tech Stack
| Layer            | Tools Used                                       |
|------------------|--------------------------------------------------|
| ML Model         | XGBoost + SMOTE                                  |
| API              | FastAPI (Python)                                 |
| Dashboard        | Streamlit (Python)                               |
| Data Streaming   | Kafka + Kafka Python client                      |
| Database         | Supabase (PostgreSQL)                            |
| Deployment       | Docker + Kubernetes (AWS EKS)                    |
| CI/CD            | GitHub Actions                                   |

---

## Project Structure
```
fraud_detection_mlops_pipeline/
├── fraud-api/              # FastAPI backend
├── streamlit-app/          # Streamlit UI
├── kafka/                  # Kafka producer + consumer
├── k8s/                    # Kubernetes manifests
├── models/                 # Trained model(s)
├── .github/workflows/      # GitHub Actions
├── README.md
```

---

## Real-Time Flow
```
Kafka Producer  →  Kafka Topic  →  Kafka Consumer  →  FastAPI API  →  Supabase DB  →  Streamlit UI
```

---

## Main Components

### 1. ML Model
- Dataset: `PaySim`
- Preprocessing: feature engineering, SMOTE for class balance
- Model: `XGBoost`
- Output: binary fraud prediction + fraud probability

### 2. FastAPI (Backend)
- Serves predictions via `/predict`
- Logs inputs + outputs to Supabase
- Dockerized and deployed on AWS EKS

### 3. Streamlit (Dashboard)
- Accepts user input
- Visualizes predictions
- Displays log history from Supabase

### 4. Kafka (Streaming)
- Producer simulates transactions
- Consumer sends data to FastAPI

### 5. Supabase
- Logs all predictions
- PostgreSQL cloud storage

### 6. CI/CD
- GitHub Actions auto-deploys on push
- Docker image → ECR → Kubernetes deployment

---


## Live Dashboard
Hosted on AWS EKS via LoadBalancer:
```
Streamlit UI:http://a66d5a3669b364837b7cb0f3d0d81336-1797693553.us-east-2.elb.amazonaws.com
FastAPI Docs:http://localhost:8000/docs#/default/predict_predict_post
```

---

## Coming Soon: GenAI-Powered Explanation Engine
I am planning to integrate LangChain + GPT to provide human-readable explanations for high-risk predictions + Live visual dashboard

---

## License
MIT License

---

## Credits
Shyam Subedi: https://github.com/ShyamSubedi as a showcase for real-world MLOps implementation using free-tier tools and services.

---

## Connect With Me
- LinkedIn: https://www.linkedin.com/in/shyam-subedi-b879b3234
- GitHub: https://github.com/ShyamSubedi
- Email: subediz420@gmail.com

