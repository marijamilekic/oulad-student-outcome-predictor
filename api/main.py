"""
FastAPI servis za baseline model.

Pokretanje (iz korena projekta):
    uvicorn api.main:app --reload --port 8000

Dokumentacija: http://localhost:8000/docs
"""

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OULAD predikcija rizika")

model = joblib.load("models/baseline_model.joblib")

FEATURE_COLS = [ "num_of_prev_attempts", "studied_credits", "module_presentation_length", "date_registration", "code_module", "gender", "region","highest_education", "imd_band", "age_band", "disability"]

# Ako neko posalje broj tamo gde treba tekst, FastAPI ce sam odbiti zahtev sa jasnom greskom
class StudentFeatures(BaseModel):
    code_module: str
    gender: str
    region: str
    highest_education: str
    imd_band: str | None = None
    age_band: str
    disability: str
    num_of_prev_attempts: int
    studied_credits: int
    module_presentation_length: int
    date_registration: float | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: StudentFeatures):
    # model_dump() pretvara pydantic obj u [dict] pa u df
    row = pd.DataFrame([features.model_dump()])
    row = row[FEATURE_COLS]

    probability = model.predict_proba(row)[0, 1]

    return {
        "at_risk_probability": round(float(probability), 4),
        "at_risk_prediction": int(probability >= 0.5),
    }