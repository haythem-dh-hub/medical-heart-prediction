import pandas as pd
from pathlib import Path
from src.config import RAW_DATA_PATH


def load_dataset(file_path: Path | str | None = None) -> pd.DataFrame:
    path = Path(file_path) if file_path else RAW_DATA_PATH
    
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Please check the data/archive directory."
        )

    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)
