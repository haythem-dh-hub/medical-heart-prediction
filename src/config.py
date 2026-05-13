from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_ARCHIVE_DIR = BASE_DIR / "data" / "archive"
RAW_DATA_PATH = DATA_ARCHIVE_DIR / "brfss_2020_2024_pooled_eda.parquet"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "heart_risk_model.joblib"
FEATURES_PATH = MODEL_DIR / "feature_columns.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"
DEEP_MODEL_PATH = MODEL_DIR / "heart_risk_deep_model.keras"
DEEP_SCALER_PATH = MODEL_DIR / "deep_scaler.joblib"
DEEP_METRICS_PATH = MODEL_DIR / "deep_metrics.json"
SPARK_METRICS_PATH = MODEL_DIR / "spark_metrics.json"
TARGET_COLUMN = "target"
