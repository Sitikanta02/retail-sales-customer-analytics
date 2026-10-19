
from pathlib import Path
import pandas as pd

data_dir = Path("data/raw")
files = sorted(data_dir.glob("*.csv"))

if not files:
    print("No CSV files found. Check data/raw/")
else:
    print(f"Found {len(files)} CSV files\n")

    for file in files:
        df = pd.read_csv(file, nrows=5)

        print(f"File: {file.name}")
        print(f"Columns: {list(df.columns)}")
        print("-" * 60)
