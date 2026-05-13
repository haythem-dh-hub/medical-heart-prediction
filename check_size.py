import pandas as pd
from pathlib import Path

archive_path = Path('data/archive/brfss_2020_2024_pooled_eda.parquet')
if archive_path.exists():
    df = pd.read_parquet(archive_path)
    print(f"Total rows in pooled dataset: {len(df):,}")
    print(f"Columns: {df.columns.tolist()}")
else:
    print("Pooled dataset not found.")
