import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def gen_data():
    rows = 2_000_000
    countries = ["US", "India", "UK", "Germany", "Canada"]
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Headphones"]
    df = pd.DataFrame(
        {
            "order_id": np.arange(rows),
            "country": np.random.choice(countries, rows),
            "product": np.random.choice(products, rows),
            "price": np.random.randint(50, 1000, rows),
            "quantity": np.random.randint(1, 5, rows),
        }
    )
    df["sales"] = df["price"] * df["quantity"]
    print(df.head())
    return df


def write_data_to_lake(dataframe, path):
    os.makedirs(path, exist_ok=True)

    chunk_size = 200000
    for i in range(0, len(dataframe), chunk_size):
        chunk = dataframe.iloc[i : i + chunk_size]
        table = pa.Table.from_pandas(chunk)
        pq.write_table(table, f"lake/orders/orders_{i}.parquet")

    print("Parquet files written.")


def main():
    dataframe = gen_data()
    write_data_to_lake(dataframe, "lake/orders")


if __name__ == "__main__":
    main()
