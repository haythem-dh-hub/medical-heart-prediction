import joblib
import pandas as pd

try:
    import tensorflow as tf
except ModuleNotFoundError:
    tf = None

from src.config import (
    DEEP_METRICS_PATH,
    DEEP_MODEL_PATH,
    DEEP_SCALER_PATH,
    FEATURES_PATH,
    MODEL_PATH,
    SPARK_METRICS_PATH,
)
from src.reporting import load_metrics, load_metrics_from_path


def load_artifacts():
    if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
        raise FileNotFoundError("Missing saved model artifacts.")

    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    return model, feature_columns


def predict_risk(model, feature_columns, input_data: pd.DataFrame) -> tuple[int, float]:
    aligned = input_data.reindex(columns=feature_columns, fill_value=0)
    prediction = int(model.predict(aligned)[0])
    probability = float(model.predict_proba(aligned)[0][1])
    return prediction, probability


def load_project_summary():
    return load_metrics()


def load_deep_artifacts():
    if tf is None:
        raise FileNotFoundError("TensorFlow is not installed.")

    if (
        not DEEP_MODEL_PATH.exists()
        or not DEEP_SCALER_PATH.exists()
        or not FEATURES_PATH.exists()
    ):
        raise FileNotFoundError("Missing deep learning model artifacts.")

    model = tf.keras.models.load_model(DEEP_MODEL_PATH)
    scaler = joblib.load(DEEP_SCALER_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    return model, scaler, feature_columns


def predict_risk_deep(model, scaler, feature_columns, input_data: pd.DataFrame) -> tuple[int, float]:
    aligned = input_data.reindex(columns=feature_columns, fill_value=0)
    scaled = scaler.transform(aligned)
    probability = float(model.predict(scaled, verbose=0).flatten()[0])
    prediction = int(probability >= 0.5)
    return prediction, probability


def load_deep_summary():
    return load_metrics_from_path(DEEP_METRICS_PATH)


def load_spark_summary():
    return load_metrics_from_path(SPARK_METRICS_PATH)
