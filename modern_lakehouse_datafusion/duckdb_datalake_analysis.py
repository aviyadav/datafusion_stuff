import duckdb


def analyze_data(path, conn):
    result = conn.execute(f"SELECT count(*) FROM '{path}/orders_*.parquet'").df()
    # print(result.fetchone())
    print(result)


def sales_analysis(path, conn):
    result = conn.sql(f"""
        SELECT country, SUM(sales) AS total_sales
            FROM '{path}/orders_*.parquet'
            GROUP BY country
    """).df()
    print(result)


def product_analysis(path, conn):
    result = conn.sql(f"""
        SELECT
            product,
            SUM(sales) AS total_sales,
            COUNT(*) AS orders
        FROM '{path}/orders_*.parquet'
        GROUP BY product
    """).df()
    print(result)


if __name__ == "__main__":
    conn = duckdb.connect()
    analyze_data("lake/orders", conn)
    sales_analysis("lake/orders", conn)
    product_analysis("lake/orders", conn)
