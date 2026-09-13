"""
Trening baseline modela.

Koristi se logisticka regresija sa kojom ce se kasnije porediti slozeniji modeli.
"""

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from oulad_pipe.data.baseline import build_baseline_dataset

num_col = [ "num_of_prev_attempts", "studied_credits", "module_presentation_length", "date_registration"]
cat_col = ["code_module", "gender", "region", "highest_education", "imd_band", "age_band", "disability"]

def build_model():
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessing = ColumnTransformer([
        ("num", numeric_pipe, num_col),
        ("cat", categorical_pipe, cat_col),
    ])

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    return model


if __name__ == "__main__":
    df = build_baseline_dataset()

    feature_cols = num_col + cat_col
    X = df[feature_cols]    
    y = df["at_risk"]   

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = build_model()
    model.fit(X_train, y_train) 

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_proba))
    
    joblib.dump(model, "models/baseline_model.joblib")
    print("Model sacuvan u models/baseline_model.joblib")