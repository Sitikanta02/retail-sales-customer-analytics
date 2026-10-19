from src.extract import extract_data
from src.transform import transform_data
from src.data_quality import validate_data
from src.load import load_data


def main():
    print("Starting ETL pipeline...\n")

    # Step 1: Extract data
    datasets = extract_data()

    # Step 2: Transform data
    print("\nStarting transformation...\n")
    transformed = transform_data(datasets)

    # Step 3: Validate data quality
    print("\nRunning data-quality checks...\n")
    validate_data(transformed)

    # Step 4: Load data into PostgreSQL
    print("\nLoading data into PostgreSQL...\n")
    load_data(transformed)

    print("\nETL pipeline completed successfully!")


if __name__ == "__main__":
    main()