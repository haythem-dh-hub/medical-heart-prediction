import pandas as pd

from src.config import TARGET_COLUMN


def prepare_features(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    cleaned = dataframe.dropna().copy()

    if TARGET_COLUMN not in cleaned.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    x = cleaned.drop(columns=[TARGET_COLUMN])
    y = cleaned[TARGET_COLUMN]
    return x, y
