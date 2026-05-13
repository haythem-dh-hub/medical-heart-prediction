import json
from pathlib import Path
from typing import Any

from src.config import METRICS_PATH, MODEL_DIR


def save_metrics(metrics: dict[str, Any]) -> None:
    save_metrics_to_path(METRICS_PATH, metrics)


def save_metrics_to_path(path: Path, metrics: dict[str, Any]) -> None:
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2)


def load_metrics() -> dict[str, Any]:
    if not METRICS_PATH.exists():
        raise FileNotFoundError("Metrics file not found. Run training first.")

    with open(METRICS_PATH, "r", encoding="utf-8") as metrics_file:
        return json.load(metrics_file)


def load_metrics_from_path(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Metrics file not found at {path}.")

    with open(path, "r", encoding="utf-8") as metrics_file:
        return json.load(metrics_file)
