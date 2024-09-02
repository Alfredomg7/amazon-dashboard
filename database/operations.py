import polars as pl

def get_monthly_summary(df):
    monthly_summary = df.group_by("Month").agg([
        pl.count("Order Date").alias("total_purchases"),
        pl.sum("Amount").alias("total_amount"),
        pl.mean("Amount").alias("average_amount"),
        pl.sum("Quantity").alias("total_quantity"),
        pl.mean("Quantity").alias("average_quantity"),
        pl.mean("Purchase Price Per Unit").alias("average_price")
    ])
    monthly_summary = monthly_summary.sort("Month")
    return monthly_summary

def get_state_summary(df):
    state_summary = df.group_by("Shipping Address State").agg([
        pl.count("Order Date").alias("total_purchases"),
        pl.sum("Amount").alias("total_amount"),
        pl.mean("Amount").alias("average_amount"),
        pl.sum("Quantity").alias("total_quantity"),
        pl.mean("Quantity").alias("average_quantity"),
        pl.mean("Purchase Price Per Unit").alias("average_price")
    ])
    state_summary = state_summary.with_columns(pl.col("total_purchases").cast(pl.Int64))
    return state_summary

def get_category_summary(df, metric):
    category_summary = df.group_by("Category").agg([
        pl.count("Order Date").alias("total_purchases"),
        pl.sum("Amount").alias("total_amount"),
        pl.mean("Amount").alias("average_amount"),
        pl.sum("Quantity").alias("total_quantity"),
        pl.mean("Quantity").alias("average_quantity"),
        pl.mean("Purchase Price Per Unit").alias("average_price")
    ])
    category_summary = category_summary.sort(metric, descending=True).head(20)
    category_summary = category_summary.sort(metric)
    return category_summary

def get_metrics_data(df):
    histogram_df = df.select([
        "Amount", "Quantity", "Purchase Price Per Unit"
    ])
    return histogram_df