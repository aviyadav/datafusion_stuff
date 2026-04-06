# datafusion-demo

A small demo project showcasing basic usage of the Python DataFusion bindings together with PyArrow and PyIceberg. It contains a few example scripts that demonstrate reading/writing Parquet, converting CSV → Parquet, running SQL queries against registered CSV tables, a tiny Iceberg in-memory example, and a helper to generate a large synthetic CSV for testing.

---

## Project layout

- `main.py` — example entrypoint showing:
  - reading Parquet and simple column expressions,
  - a PyIceberg in-memory example that creates an Iceberg table and registers it with a DataFusion `SessionContext`,
  - a SQL example that registers a CSV and runs a SQL query.
- `utils.py` — helper utilities:
  - `time_it` decorator for measuring execution time,
  - `csv_to_parquet(input_csv, output_parquet)` to convert CSV to Parquet using DataFusion,
  - `download_file(url, output_path)` simple HTTP downloader (uses `requests`).
- `generate_large_pokemon.py` — multiprocessing script to synthesize a large CSV (default: 1,000,000 rows) from a smaller `pokemon.csv` dataset.
- `data/` — directory (tracked) intended to hold sample data files used by the demos (Parquet/CSV files).

---

## Requirements

- Python >= 3.13 (project `pyproject.toml` sets `requires-python = ">=3.13"`)
- The project dependencies (listed in `pyproject.toml`):
  - `datafusion>=50.1.0`
  - `pyarrow>=22.0.0`
  - `pyiceberg-core>=0.7.0`
  - `pyiceberg[sql-sqlite]>=0.10.0`
  - `requests>=2.32.5`

Tip: Installing from the `pyproject.toml` using pip will pull the declared dependencies:
- From the project root:
  - Create a venv:
    - Windows:
      - `python -m venv .venv`
      - `.venv\Scripts\activate`
    - macOS/Linux:
      - `python -m venv .venv`
      - `source .venv/bin/activate`
  - Install:
    - `pip install .`

Alternatively, install dependencies manually with `pip install datafusion pyarrow pyiceberg-core "pyiceberg[sql-sqlite]" requests`

Note: DataFusion and PyArrow are native packages that may require compatible platform wheels. If you see build errors, ensure you are using a supported Python version and have a compatible wheel available for your platform.

---

## Usage examples

1. Quick SQL example (as implemented in `main.py`):
   - The `sql_ex()` function registers `data/pokemon.csv` as a CSV table named `pokemon` and executes:
     - `SELECT "Attack"+"Defense", "Attack"-"Defense" FROM pokemon`
   - Run:
     - `python main.py`
   - By default `main.py` calls `sql_ex()` when executed directly. Uncomment other calls at the bottom of `main.py` to run them instead.

2. Parquet read + expression example:
   - `main()` (commented out by default) demonstrates reading a Parquet file (`data/yellow_tripdata_2021-01.parquet`) and selecting:
     - `trip_distance`, `total_amount` as `total`, and a computed `tip_percentage`.
   - To try:
     - Download a Parquet file into `data/` (or convert one from CSV) and run `python main.py` after switching the entry in the `if __name__ == "__main__":` block.

3. CSV → Parquet conversion:
   - Use the helper in `utils.py`:
     - Example:
       - `from utils import csv_to_parquet`
       - `csv_to_parquet("data/pokemon_million.csv", "data/pokemon_million.parquet")`
   - The helper uses DataFusion's CSV reader and writes a Parquet with Snappy compression.

4. Download a remote Parquet:
   - Use `download_file` in `utils.py`:
     - Example:
       - `from utils import download_file`
       - `download_file("https://.../yellow_tripdata_2021-01.parquet", "data/yellow_tripdata_2021-01.parquet")`

Some examples rely on data which can be downloaded from the following site:

- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Here is a direct link to the file used in the examples:

- https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet


5. Iceberg in-memory example:
   - The `iceberg_ex()` function in `main.py` shows using `pyiceberg.catalog.load_catalog("catalog", type="in-memory")` to create a namespace and table, append a small Arrow table, register it with DataFusion, and read it via `SessionContext`.
   - This demonstrates integration points; for production Iceberg usage you would point the PyIceberg catalog to a real backend.

6. Generate a large synthetic CSV (stress testing):
   - `python generate_large_pokemon.py`
   - By default it creates `pokemon_million.csv` with ~1,000,000 rows (adjustable in the script). Uses multiple processes to speed up generation.

---

## Example: reading a parquet and showing a few columns (conceptual)

The `main.py` file contains this snippet (simplified):

- Create a DataFusion `SessionContext`
- Read Parquet:
  - `df = ctx.read_parquet("data/yellow_tripdata_2021-01.parquet")`
- Select columns and computed column:
  - `df = df.select("trip_distance", col("total_amount").alias("total"), (f.round(lit(100.0) * col("tip_amount") / col("total_amount"), lit(1))).alias("tip_percentage"))`
- `df.show()` to print sample rows

---

## Notes & troubleshooting

- Python version: make sure you run Python >= 3.13 as declared in `pyproject.toml`.
- DataFusion occasionally has platform-specific wheel availability — installing on less common platforms may require building from source or using a compatible wheel. If pip fails to find a wheel, check the DataFusion project for platform support or try a different Python minor version that has pre-built wheels.
- If you plan to use Iceberg with a persistent catalog/backend, read the PyIceberg docs for configuring a catalog (S3, Hive metastore, SQLite-backed catalogs, etc.). The example here uses an in-memory catalog purely for demonstration.
- When converting big CSVs to Parquet, ensure you have sufficient memory and temporary disk space.

---

## Extending this repo

- Add more sample datasets under `data/`.
- Add Jupyter notebooks demonstrating interactive exploration (there is a `datafusion_datalake_demo.ipynb` in the sibling project — you can adapt notebook patterns here).
- Add CI that checks import and a few smoke tests that create a `SessionContext`, register a tiny table, and execute simple queries to ensure runtime dependencies are available.

---

## License

This repository is provided as a small demo. No specific license file is included — add one if you intend to redistribute.

---
