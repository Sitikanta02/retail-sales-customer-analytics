
import pandas as pd


def transform_data(datasets):
    """Clean and validate the extracted datasets."""

    transformed = {}

    # Clean each dataset without modifying the original DataFrame.
    for name, df in datasets.items():
        df = df.copy()

        # Standardize column names.
        df.columns = (
            df.columns.str.strip().str.lower()
        )

        # Remove completely duplicated rows.
        duplicate_count = int(df.duplicated().sum())
        df = df.drop_duplicates()

        transformed[name] = df

        print(
            f"{name}: removed {duplicate_count:,} "
            f"duplicate rows; {len(df):,} rows remaining"
        )

    # Validate essential identifiers.
    required_columns = {
        "orders": ["order_id", "customer_id"],
        "customers": ["customer_id"],
        "order_items": ["order_id", "product_id", "seller_id"],
        "order_payments": ["order_id"],
        "products": ["product_id"],
        "sellers": ["seller_id"],
    }

    for dataset_name, columns in required_columns.items():
        if dataset_name not in transformed:
            continue

        df = transformed[dataset_name]

        for column in columns:
            if column in df.columns:
                missing = int(df[column].isna().sum())

                if missing:
                    print(
                        f"WARNING: {dataset_name}.{column} "
                        f"has {missing:,} missing values"
                    )

    # Convert order timestamps to datetime.
    if "orders" in transformed:
        date_columns = [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]

        df = transformed["orders"]

        for column in date_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

        transformed["orders"] = df

    # Check for invalid monetary values.
    for dataset_name, column in [
        ("order_items", "price"),
        ("order_items", "freight_value"),
        ("order_payments", "payment_value"),
    ]:
        if dataset_name in transformed:
            df = transformed[dataset_name]

            if column in df.columns:
                invalid_count = int(
                    (df[column] < 0).sum()
                )

                if invalid_count:
                    print(
                        f"WARNING: {dataset_name}.{column} "
                        f"has {invalid_count:,} negative values"
                    )

    return transformed
