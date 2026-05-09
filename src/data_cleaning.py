# =============================================================================
# data_cleaning.py
# Purpose: Clean a messy raw sales dataset and export a processed version.
# This script standardizes column names, strips whitespace, handles missing
# values, and removes invalid rows so the data is ready for analysis.
# =============================================================================

import pandas as pd


# -----------------------------------------------------------------------------
# FUNCTION: load_data
# Reads a CSV file from the given path and returns it as a DataFrame.
# Loading through a function makes it easy to swap file paths or add
# error handling later without touching the rest of the pipeline.
# -----------------------------------------------------------------------------
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows from {file_path}")
    return df


# -----------------------------------------------------------------------------
# FUNCTION: clean_column_names
# Converts all column headers to lowercase with underscores and removes any
# surrounding whitespace. Consistent column names prevent KeyError bugs and
# make the rest of the code easier to read.
# -----------------------------------------------------------------------------
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()          # remove leading/trailing spaces
        .str.lower()          # make everything lowercase
        .str.replace(" ", "_")  # replace spaces with underscores
    )
    print("Column names cleaned:", list(df.columns))
    return df


# -----------------------------------------------------------------------------
# FUNCTION: handle_missing_values
# Drops rows where both price AND quantity are missing, because a sales record
# with no price and no quantity has no analytical value. For rows missing only
# one of the two, we fill the missing value with the column median so we keep
# as many records as possible without inventing numbers.
# We also strip whitespace from text columns so " electronics " and
# "electronics" are treated as the same category.
# -----------------------------------------------------------------------------
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Strip whitespace from string columns
    # Why: raw data often has invisible spaces that cause grouping errors
    for col in ["prod_name", "category"]:
        if col in df.columns:
            df[col] = df[col].str.strip()

    # Drop rows where BOTH price and qty are missing
    # Why: no quantity and no price means the row is completely useless
    df = df.dropna(subset=["price", "qty"], how="all")

    # Convert price and qty to numeric, forcing any leftover text/spaces to NaN
    # Why: the raw CSV has spaces around numbers that prevent math operations
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

    # Fill remaining missing prices with the median price
    # Why: median is resistant to outliers and keeps the row in the dataset
    df["price"] = df["price"].fillna(df["price"].median())

    # Fill remaining missing quantities with 1 (assume at least one was sold)
    # Why: a sales record almost certainly represents at least one item sold
    df["qty"] = df["qty"].fillna(1)

    print(f"After handling missing values: {len(df)} rows remain")
    return df


# -----------------------------------------------------------------------------
# FUNCTION: remove_invalid_rows
# Removes rows with negative prices or negative quantities.
# Why: negative prices and negative quantities are data-entry errors.
# A sale cannot have a negative count of items or a negative selling price.
# We also remove exact duplicate rows to avoid double-counting sales.
# -----------------------------------------------------------------------------
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    # Remove rows where quantity is zero or negative
    df = df[df["qty"] > 0]

    # Remove rows where price is zero or negative
    df = df[df["price"] > 0]

    # Remove exact duplicate rows
    # Why: the same sale recorded twice inflates totals
    df = df.drop_duplicates()

    print(f"Removed {before - len(df)} invalid/duplicate rows. {len(df)} rows remain.")
    return df


# -----------------------------------------------------------------------------
# MAIN PIPELINE
# Runs all cleaning steps in order and saves the result.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    raw_path = r"C:\Users\Jessi\OneDrive\Desktop\Spring 2026\Python for Business\ism2411-data-cleaning-copilot\data\raw\sales_data_raw.csv"
    cleaned_path = r"C:\Users\Jessi\OneDrive\Desktop\Spring 2026\Python for Business\ism2411-data-cleaning-copilot\data\processed\sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)

    df_clean.to_csv(cleaned_path, index=False)
    print("\nCleaning complete. First few rows:")
    print(df_clean.head())
