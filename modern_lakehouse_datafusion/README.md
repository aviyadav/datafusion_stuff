# Modern Lakehouse — DataFusion Demo

This repository contains a lightweight demo showing how to explore building a modern lakehouse-style workflow using Apache Arrow / PyArrow and the Rust DataFusion Python bindings. The demo is focused around an interactive Jupyter notebook that walks through reading parquet/CSV data, simple transforms with DataFusion, and some lightweight visualization.

This project is intended as a learning/demo sandbox — not a production system.

---

## Contents

- `datafusion_datalake_demo.ipynb` — The primary interactive notebook. The notebook demonstrates reading Parquet/CSV, performing SQL and DataFrame-style operations via the `datafusion` Python bindings, and a few example visualizations.
- `main.py` — Script to generate sample order data and write it to Parquet files in the lakehouse structure.
- `duckdb_datalake_analysis.py` — Script to analyze the generated Parquet data using DuckDB for SQL queries and aggregations.
- `pyproject.toml` — Project metadata and dependency pinning used to show compatible package versions.
- `.python-version` — Recommended Python version for the repo (see Requirements).
- `.gitignore`, `uv.lock` — VCS and lockfiles.

---

## Goals

- Demonstrate how to use DataFusion and DuckDB in Python to read Arrow/Parquet data and run SQL operations.
- Show a minimal "lakehouse" style flow: read storage file(s), apply schema-aware transforms, and visualize aggregated results.
- Keep the demo small and easy to run locally.

---

## Requirements

- Python 3.14+ (see `pyproject.toml`)
- The Python packages listed in `pyproject.toml`:
  - `datafusion>=52.3.0`
  - `duckdb>=1.1.0`
  - `jupyter>=1.1.1`
  - `numpy>=2.0.0`
  - `pandas>=3.0.2`
  - `plotly>=6.6.0`
  - `pyarrow>=23.0.1`

You can install these directly with `pip` (example shown below) or use your preferred environment/poetry/pip-tools workflow.

---

## Quick setup

1. Create and activate a virtual environment:

   - Create: `python -m venv .venv`
   - Activate:
     - macOS / Linux: `source .venv/bin/activate`
     - Windows (PowerShell): `.venv\\Scripts\\Activate.ps1`
     - Windows (cmd): `.venv\\Scripts\\activate.bat`

2. Install the runtime dependencies (example with `pip`):

   - `pip install "datafusion>=52.3.0" "duckdb>=1.1.0" "jupyter>=1.1.1" "numpy>=2.0.0" "pandas>=3.0.2" "plotly>=6.6.0" "pyarrow>=23.0.1"`

   Note: If you use a dependency manager (Poetry/Flit/pip-tools) prefer that flow and use `pyproject.toml`.

3. (Optional) Generate sample data:

   - Run `python main.py` to create Parquet files in the `lake/orders/` directory.

4. (Optional) Run DuckDB analysis:

   - Run `python duckdb_datalake_analysis.py` to analyze the generated data with SQL queries.

5. Launch the notebook:

   - `jupyter notebook` or `jupyter lab` then open `datafusion_datalake_demo.ipynb`

---

## Data Generation

The `main.py` script generates synthetic order data (2 million rows) including order ID, country, product, price, quantity, and sales. It writes the data to partitioned Parquet files in `lake/orders/` for lakehouse-style storage.

- Run with: `python main.py`
- Output: Parquet files like `orders_0.parquet`, `orders_200000.parquet`, etc.

## DuckDB Analysis

The `duckdb_datalake_analysis.py` script demonstrates querying the Parquet lakehouse using DuckDB's SQL engine with wildcard support.

- Run with: `python duckdb_datalake_analysis.py`
- Performs: Row count, sales by country, and sales by product aggregations.

## Notebook / Demo notes

- The notebook shows:
  - How to create a `datafusion.SessionContext`.
  - Reading Parquet and CSV datasets with DataFusion (`ctx.read_parquet`, `ctx.read_csv`).
  - Running SQL queries using `ctx.sql(...)` and using the DataFrame-style API.
  - Converting results to Pandas for visualization with `plotly` when helpful.
  - A minimal demonstration of registering external table providers (Arrow tables / PyIceberg examples can be sketched in the notebook).

- If you want to run heavy data operations locally:
  - Make sure the input Parquet/CSV files exist and are accessible from the notebook environment.
  - For testing, try small sample files first to validate functionality.

---

## Example usage patterns (illustrative; run inside a notebook)

- Create a session and read parquet:

  - `ctx = SessionContext()`
  - `df = ctx.read_parquet("path/to/file.parquet")`

- Run a SQL query:

  - `df = ctx.sql("SELECT col1, SUM(col2) FROM table GROUP BY col1")`

- Use DataFrame-style expressions:

  - `from datafusion import col, lit, functions as f`
  - `df = df.select("trip_distance", col("total_amount").alias("total"))`

- Convert to Pandas for plotting:

  - `pandas_df = df.to_pandas()`
  - Use `plotly` or `pandas` plotting utilities to visualize.

---

## Development tips

- If you get version or C-extension related errors for `datafusion` or `pyarrow`, verify:
  - Your Python version matches what's expected (see `.python-version` and `pyproject.toml`).
  - The platform wheels are available for the `datafusion` version you're installing. On some platforms you may need to match `pyarrow` and `datafusion` binary compatibility.

- Reproducible environments:
  - Consider using `poetry` or pinned `requirements.txt` and a lockfile to make local reproduction easier.
  - If you need to test different `datafusion` versions, create separate virtual environments.

---

## Extending this demo

Ideas for next steps you may want to add:

- Add a loader module to convert CSV -> Parquet in a reproducible way (the `datafusion-demo` sibling repo contains such helpers as inspiration).
- Add a small local Iceberg catalog example (using `pyiceberg`) for table management.
- Add more advanced query patterns, e.g. window functions, joins across partitioned parquet datasets, and query planning introspection.
- Compare query performance between DataFusion and DuckDB for the same datasets and operations.
- Extend the DuckDB analysis to include persistent database storage, user-defined functions, or integration with other data sources.
- Create a unified script that uses both DataFusion for in-memory processing and DuckDB for disk-based analytics.

---

## Troubleshooting

- If `jupyter` refuses to start or kernel errors occur, ensure the virtual environment is active and the kernel points at the same Python interpreter.
- For DataFusion-specific runtime errors:
  - Check installed package versions.
  - Consult DataFusion Python binding docs and the `pyarrow` compatibility notes.
- For DuckDB-specific runtime errors:
  - Ensure the Parquet files exist and the path is correct.
  - Check that the wildcard pattern matches the file names (e.g., `orders_*.parquet`).
  - Verify DuckDB version compatibility with Parquet format and PyArrow.

---

## License

This demo repository is intended for examples and learning. No license file is included by default; add one if you plan to publish or share under specific terms.

---

If you want, I can:
- Add a short runnable `examples/` script that reproduces the main notebook actions in plain Python.
- Generate a `requirements.txt` or `poetry.lock` to make environment creation reproducible.
- Add a short troubleshooting/FAQ section for common DataFusion + PyArrow issues on different OSes.
