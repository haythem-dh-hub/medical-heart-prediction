import pandas as pd
try:
    df = pd.read_parquet('data/archive/brfss_2020_2024_pooled_eda.parquet')
    with open('columns.txt', 'w') as f:
        f.write('\n'.join(df.columns.tolist()))
except Exception as e:
    with open('columns.txt', 'w') as f:
        f.write(str(e))
