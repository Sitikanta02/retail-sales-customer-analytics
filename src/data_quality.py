
def validate_data(datasets):
    """Run automated data-quality checks on transformed datasets."""

    errors = []

    def check(condition, message):
        if condition:
            print(f"PASS: {message}")
        else:
            print(f"FAIL: {message}")
            errors.append(message)

    # 1. Required identifiers must not be missing.
    required_columns = {
        "orders": ["order_id", "customer_id"],
        "customers": ["customer_id"],
        "order_items": ["order_id", "order_item_id", "product_id", "seller_id"],
        "order_payments": ["order_id"],
        "products": ["product_id"],
        "sellers": ["seller_id"],
    }

    for dataset_name, columns in required_columns.items():
        df = datasets[dataset_name]

        for column in columns:
            check(
                column in df.columns
                and df[column].notna().all(),
                f"{dataset_name}.{column} exists and has no missing values",
            )

    # 2. Primary-key uniqueness.
    unique_keys = {
        "orders": ["order_id"],
        "customers": ["customer_id"],
        "products": ["product_id"],
        "sellers": ["seller_id"],
        "order_items": ["order_id", "order_item_id"],
    }

    for dataset_name, columns in unique_keys.items():
        df = datasets[dataset_name]

        unique = (
            all(column in df.columns for column in columns)
            and not df.duplicated(subset=columns).any()
        )

        check(
            unique,
            f"{dataset_name} has unique key: {', '.join(columns)}",
        )

    # 3. Foreign-key relationships.
    relationships = [
        ("orders", "customer_id", "customers", "customer_id"),
        ("order_items", "order_id", "orders", "order_id"),
        ("order_items", "product_id", "products", "product_id"),
        ("order_items", "seller_id", "sellers", "seller_id"),
        ("order_payments", "order_id", "orders", "order_id"),
        ("order_reviews", "order_id", "orders", "order_id"),
    ]

    for child_name, child_col, parent_name, parent_col in relationships:
        child = datasets[child_name]
        parent = datasets[parent_name]

        unmatched = ~child[child_col].isin(parent[parent_col])

        check(
            not unmatched.any(),
            f"{child_name}.{child_col} matches {parent_name}.{parent_col}",
        )

    # 4. Monetary values must be non-negative.
    for dataset_name, column in [
        ("order_items", "price"),
        ("order_items", "freight_value"),
        ("order_payments", "payment_value"),
    ]:
        df = datasets[dataset_name]

        check(
            df[column].notna().all() and df[column].ge(0).all(),
            f"{dataset_name}.{column} is non-negative and not missing",
        )

    # 5. Report final status.
    if errors:
        raise ValueError(
            f"Data-quality validation failed: {len(errors)} check(s)."
        )

    print("\nAll data-quality checks passed!")
