
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_engine():
    """Create a PostgreSQL connection engine."""

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "retail_analytics"),
    )

    return create_engine(connection_url)


def load_data(datasets):
    """Load transformed DataFrames into PostgreSQL tables."""

    engine = get_engine()

    try:
        with engine.connect() as connection:
            print(
                "Connected to PostgreSQL:",
                connection.execute(
                    __import__("sqlalchemy").text(
                        "SELECT current_database()"
                    )
                ).scalar_one(),
            )

        for name, df in datasets.items():
            table_name = f"stg_{name}"

            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False,
                chunksize=5000,
                method="multi",
            )

            print(
                f"Loaded {len(df):,} rows into {table_name}"
            )

    finally:
        engine.dispose()


if __name__ == "__main__":
    print("Run the loader through src.main.")
