from unittest import result
from datafusion import SessionContext, col, lit, functions as f
from utils import time_it, csv_to_parquet, download_file

from pyiceberg.catalog import load_catalog
import pyarrow as pa


@time_it
def main():
    ctx = SessionContext()
    # df = ctx.read_parquet("data/pokemon_million.parquet")
    # df.show()

    df = ctx.read_parquet("data/yellow_tripdata_2021-01.parquet")
    df = df.select(
        "trip_distance",
        col("total_amount").alias("total"),
        (f.round(lit(100.0) * col("tip_amount") / col("total_amount"), lit(1))).alias("tip_percentage"),
    )

    df.show()

def iceberg_ex():
    catalog = load_catalog("catalog", type="in-memory")
    catalog.create_namespace_if_not_exists("default")

    # locad csv into iceberg table
    # df = pa.csv.read_csv("data/pokemon_million.csv").to_table() 

    data = pa.table({"x": [1, 2, 3], "y": [4, 5, 6]})
    iceberg_table = catalog.create_table(
        identifier="default.test",
        schema=data.schema,
    )
    iceberg_table.append(data)

    ctx = SessionContext()
    ctx.register_table_provider("test", iceberg_table)

    ctx.table("test").show()

def sql_ex():
    ctx = SessionContext()
    ctx.register_csv("pokemon", "data/pokemon.csv")
    df = ctx.sql('SELECT "Attack"+"Defense", "Attack"-"Defense" FROM pokemon')

    df.show()


if __name__ == "__main__":
    # csv_to_parquet("data/pokemon_million.csv", "data/pokemon_million.parquet")
    # download_file("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet", "data/yellow_tripdata_2021-01.parquet")
    # main()
    # iceberg_ex()
    sql_ex()
