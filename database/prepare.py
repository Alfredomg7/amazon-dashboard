import polars as pl

def add_calculated_fields(df):
    df = df.with_columns(
        pl.col("Order Date").str.slice(0, 7).alias("Month"),
        (pl.col("Purchase Price Per Unit") * pl.col("Quantity")).alias("Amount")
    )
    return df

def create_binned_data(df):
    df = df.with_columns([
        pl.when(pl.col("Amount") > 100)
        .then(pl.lit(">100"))
        .otherwise(((pl.col("Amount") // 10) * 10).cast(str))
        .alias("Amount"),

        pl.when(pl.col("Purchase Price Per Unit") > 100)
        .then(pl.lit(">100"))
        .otherwise(((pl.col("Purchase Price Per Unit") // 10) * 10).cast(str))
        .alias("Purchase Price Per Unit"),

        pl.when(pl.col("Quantity") > 100)
        .then(pl.lit(">100"))
        .otherwise(((pl.col("Quantity") // 10) * 10).cast(str))
        .alias("Quantity")
    ])

    amount_df = df.group_by("Amount").agg(pl.len().alias("Count")).with_columns(
        (pl.col("Amount").str.extract(r'(\d+)', 1).cast(int).fill_nan(101)).alias("sort_key")
    ).sort("sort_key").select(["Amount", "Count"])

    price_df = df.group_by("Purchase Price Per Unit").agg(pl.len().alias("Count")).with_columns(
        (pl.col("Purchase Price Per Unit").str.extract(r'(\d+)', 1).cast(int).fill_nan(101)).alias("sort_key")
    ).sort("sort_key").select(["Purchase Price Per Unit", "Count"])

    quantity_df = df.group_by("Quantity").agg(pl.len().alias("Count")).with_columns(
        (pl.col("Quantity").str.extract(r'(\d+)', 1).cast(int).fill_nan(101)).alias("sort_key")
    ).sort("sort_key").select(["Quantity", "Count"])

    return amount_df, price_df, quantity_df

def prepare_purchases_data(df):
    df = add_calculated_fields(df)
    return df

def prepare(input_path, output_paths):
    df = pl.read_csv(input_path)
    df = prepare_purchases_data(df)
    amount_df, price_df, quantity_df = create_binned_data(df)
    df.write_csv(output_paths['all_data'])
    amount_df.write_csv(output_paths['amount_histogram'])
    price_df.write_csv(output_paths['price_histogram'])
    quantity_df.write_csv(output_paths['quantity_histogram'])

if __name__ == '__main__':
    purchases_file_path = 'data/amazon-purchases.csv'
    output_file_paths = {
        'all_data': 'data/amazon-purchases-prepared.csv',
        'amount_histogram': 'data/amount_histogram.csv',
        'price_histogram': 'data/price_histogram.csv',
        'quantity_histogram': 'data/quantity_histogram.csv'
    }

    prepare(purchases_file_path, output_file_paths)
