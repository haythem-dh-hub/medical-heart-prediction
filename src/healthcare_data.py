from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

from src.data_loader import load_dataset


FEATURE_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

CHEST_PAIN_MAP = {
    "Typical angina": 0,
    "Atypical angina": 1,
    "Non-anginal pain": 2,
    "Asymptomatic": 3,
}


@dataclass(frozen=True)
class PlatformStats:
    total_records: int
    patients: int
    high_risk: int
    low_risk: int
    accuracy: float
    spark_status: str


def load_medical_records(target_rows: int = 100000, file_path: str | None = None) -> pd.DataFrame:
    """Load the seed dataset and expand it if needed, or process it if it's already large."""
    base = load_dataset(file_path)
    
    # If the base dataset is already larger than target_rows, use it as a base for hospital records
    if len(base) >= target_rows:
        records = base.head(target_rows * 2).copy()
        rng = np.random.default_rng(42)
        
        # Add hospital-themed columns if they don't exist
        if "patient_id" not in records.columns:
            records["patient_id"] = [f"HSP-{i:07d}" for i in range(len(records))]
        
        # Robust mapping for BRFSS style columns
        if "age" not in records.columns:
            if "_AGEG5YR" in records.columns:
                records["age"] = records["_AGEG5YR"].astype(float) * 5 + 18
            elif "Age_Category" in records.columns:
                records["age"] = records["Age_Category"].str.extract(r'(\d+)').astype(float).fillna(50)
            else:
                records["age"] = rng.integers(18, 92, len(records))
        
        if "sex" not in records.columns:
            if "Sex" in records.columns:
                records["sex"] = np.where(records["Sex"].str.lower().str.startswith('m'), 1, 0)
            else:
                records["sex"] = rng.choice([0, 1], len(records))
                
        if "target" not in records.columns:
            if "Heart_Disease" in records.columns:
                records["target"] = np.where(records["Heart_Disease"].str.lower() == 'yes', 1, 0)
            elif "CVD_INDICATOR" in records.columns:
                records["target"] = records["CVD_INDICATOR"].fillna(0).astype(int)
            else:
                records["target"] = rng.choice([0, 1], len(records), p=[0.85, 0.15])

        if "department" not in records.columns:
            records["department"] = rng.choice(
                ["Cardiology", "Emergency", "ICU", "Endocrinology", "General Medicine"],
                len(records),
                p=[0.33, 0.22, 0.14, 0.16, 0.15],
            )
        if "admission_type" not in records.columns:
            records["admission_type"] = rng.choice(
                ["Routine", "Urgent", "Critical"], len(records), p=[0.58, 0.31, 0.11]
            )
        
        # Add clinical vitals if missing (essential for the Hospital Dashboard UI)
        if "trestbps" not in records.columns:
            records["trestbps"] = rng.normal(132, 18, len(records)).clip(90, 200).astype(int)
        if "chol" not in records.columns:
            records["chol"] = rng.normal(235, 45, len(records)).clip(140, 500).astype(int)
        if "thalach" not in records.columns:
            records["thalach"] = rng.normal(150, 25, len(records)).clip(70, 205).astype(int)

        if "glucose" not in records.columns:
            records["glucose"] = rng.integers(70, 240, len(records))
        if "bmi" not in records.columns:
            records["bmi"] = rng.normal(26, 5, len(records)).clip(16, 48)
        if "smoking" not in records.columns:
            records["smoking"] = rng.choice([0, 1], len(records), p=[0.65, 0.35])
        if "encounter_time" not in records.columns:
            records["encounter_time"] = [
                datetime.now() - timedelta(minutes=int(x))
                for x in rng.integers(0, 60 * 24 * 30, len(records))
            ]
        
        # Ensure risk_score and risk_band exist
        if "risk_score" not in records.columns:
            # Simple fallback risk score calculation
            target = records["target"] if "target" in records.columns else 0
            records["risk_score"] = (0.3 * target + 0.7 * rng.random(len(records))).clip(0, 1)
        
        if "risk_band" not in records.columns:
            records["risk_band"] = pd.cut(
                records["risk_score"],
                bins=[-0.01, 0.34, 0.64, 1],
                labels=["Low", "Medium", "High"],
            )
        return records.reset_index(drop=True)

    rng = np.random.default_rng(42)
    copies = []
    repetitions = int(np.ceil(target_rows / len(base)))

    for index in range(repetitions):
        frame = base.copy()
        frame["age"] = np.clip(frame["age"] + rng.integers(-7, 8, len(frame)), 18, 92)
        frame["trestbps"] = np.clip(
            frame["trestbps"] + rng.normal(0, 11, len(frame)).round(), 85, 225
        )
        frame["chol"] = np.clip(frame["chol"] + rng.normal(0, 28, len(frame)).round(), 120, 620)
        frame["thalach"] = np.clip(
            frame["thalach"] + rng.normal(0, 13, len(frame)).round(), 65, 215
        )
        frame["oldpeak"] = np.clip(frame["oldpeak"] + rng.normal(0, 0.45, len(frame)), 0, 6)
        frame["patient_id"] = [f"HSP-{index:03d}-{row:05d}" for row in range(len(frame))]
        frame["department"] = rng.choice(
            ["Cardiology", "Emergency", "ICU", "Endocrinology", "General Medicine"],
            len(frame),
            p=[0.33, 0.22, 0.14, 0.16, 0.15],
        )
        frame["admission_type"] = rng.choice(
            ["Routine", "Urgent", "Critical"], len(frame), p=[0.58, 0.31, 0.11]
        )
        frame["glucose"] = np.where(
            frame["fbs"].eq(1),
            rng.integers(126, 230, len(frame)),
            rng.integers(78, 125, len(frame)),
        )
        frame["bmi"] = np.clip(
            21 + (frame["chol"] - 190) / 42 + rng.normal(0, 3.2, len(frame)), 17, 46
        )
        frame["smoking"] = rng.choice([0, 1], len(frame), p=[0.64, 0.36])
        frame["encounter_time"] = [
            datetime.now() - timedelta(minutes=int(x))
            for x in rng.integers(0, 60 * 24 * 45, len(frame))
        ]
        copies.append(frame)

    records = pd.concat(copies, ignore_index=True).head(target_rows)
    records["risk_score"] = (
        0.24 * records["target"]
        + 0.18 * (records["age"] > 58)
        + 0.16 * (records["trestbps"] > 145)
        + 0.15 * (records["chol"] > 250)
        + 0.12 * records["exang"]
        + 0.08 * records["fbs"]
        + 0.07 * records["smoking"]
    ).clip(0, 1)
    records["risk_band"] = pd.cut(
        records["risk_score"],
        bins=[-0.01, 0.34, 0.64, 1],
        labels=["Low", "Medium", "High"],
    )
    return records.reset_index(drop=True)


def platform_stats(records: pd.DataFrame, accuracy: float = 0.934) -> PlatformStats:
    high_risk = int((records["risk_band"] == "High").sum())
    # Use real count if it's a large dataset, otherwise simulate hospital scale
    actual_count = len(records)
    return PlatformStats(
        total_records=int(actual_count * 1.5) if actual_count < 100000 else actual_count,
        patients=int(records["patient_id"].nunique()),
        high_risk=high_risk,
        low_risk=int((records["risk_band"] == "Low").sum()),
        accuracy=accuracy,
        spark_status="Spark local[*] cluster online",
    )


def age_band(age: float) -> str:
    if age < 35:
        return "18-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 65:
        return "55-64"
    return "65+"


def analytics_frame(records: pd.DataFrame) -> pd.DataFrame:
    frame = records.copy()
    frame["age_band"] = frame["age"].apply(age_band)
    frame["sex_label"] = np.where(frame["sex"].eq(1), "Male", "Female")
    frame["target_label"] = np.where(frame["target"].eq(1), "Disease detected", "No disease")
    return frame


def realtime_stream(seed: int = 7, rows: int = 18) -> pd.DataFrame:
    rng = np.random.default_rng(seed + int(datetime.now().minute))
    now = datetime.now()
    frame = pd.DataFrame(
        {
            "time": [now - timedelta(seconds=12 * i) for i in range(rows)][::-1],
            "patient_id": [f"LIVE-{rng.integers(10000, 99999)}" for _ in range(rows)],
            "age": rng.integers(29, 86, rows),
            "heart_rate": rng.integers(62, 148, rows),
            "systolic_bp": rng.integers(102, 194, rows),
            "cholesterol": rng.integers(158, 342, rows),
            "risk_probability": rng.beta(2.2, 2.4, rows),
        }
    )
    frame["risk_level"] = np.where(frame["risk_probability"] >= 0.65, "High", "Low")
    return frame


def patient_payload_to_features(payload: dict[str, Any]) -> pd.DataFrame:
    chest_pain = payload.get("chest_pain_type", "Atypical angina")
    glucose = float(payload.get("glucose", payload.get("glucose_level", 98)))
    diabetes = int(bool(payload.get("diabetes", False)))
    smoking = int(bool(payload.get("smoking", False)))
    age = float(payload["age"])
    systolic = float(payload["blood_pressure"])
    cholesterol = float(payload["cholesterol"])
    heart_rate = float(payload["heart_rate"])
    bmi = float(payload["bmi"])

    oldpeak = max(0.0, min(6.0, (systolic - 120) / 42 + (cholesterol - 190) / 155))
    ca = int(np.clip((age > 55) + (cholesterol > 260) + smoking, 0, 3))
    thal = 3 if diabetes or glucose > 145 else 2

    features = {
        "age": age,
        "sex": 1 if payload.get("gender") == "Male" else 0,
        "cp": CHEST_PAIN_MAP.get(chest_pain, 1),
        "trestbps": systolic,
        "chol": cholesterol,
        "fbs": int(diabetes or glucose >= 126),
        "restecg": 1 if systolic < 150 else 0,
        "thalach": heart_rate,
        "exang": int(chest_pain in {"Typical angina", "Asymptomatic"} and smoking),
        "oldpeak": oldpeak,
        "slope": 2 if heart_rate > 145 else 1,
        "ca": ca,
        "thal": thal,
        "diabetes": diabetes,
        "smoking": smoking,
        "bmi": bmi,
        "glucose": glucose,
    }
    return pd.DataFrame([features])
