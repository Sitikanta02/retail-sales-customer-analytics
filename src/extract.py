
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def extract_data():
    """Read all raw CSV files and return them as DataFrames."""

    datasets = {}

    for file_path in sorted(RAW_DATA_DIR.glob("*.csv")):
        try:
            df = pd.read_csv(file_path)

            dataset_name = file_path.stem.replace(
                "olist_", ""
            ).replace("_dataset", "")

            datasets[dataset_name] = df

            print(
                f"Extracted {file_path.name}: "
                f"{len(df):,} rows, {len(df.columns)} columns"
            )

        except Exception as error:
            raise RuntimeError(
                f"Failed to read {file_path.name}: {error}"
            ) from error

    if not datasets:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_DIR}"
        )

    return datasets


if __name__ == "__main__":
    extract_data()
