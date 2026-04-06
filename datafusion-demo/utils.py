from functools import wraps
from timeit import default_timer as timer


def time_it(func):
    """Decorator to measure execution time of a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        print(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

def csv_to_parquet(input_csv, output_parquet):
    """Convert a CSV file to Parquet format using DataFusion"""
    from datafusion import SessionContext

    ctx = SessionContext()
    df = ctx.read_csv(input_csv)
    df.write_parquet(output_parquet, compression='snappy')

    print(f"Converted {input_csv} to {output_parquet}")

def download_file(url, output_path):
    """Download a file from a URL to a local path"""
    import requests

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded file from {url} to {output_path}")