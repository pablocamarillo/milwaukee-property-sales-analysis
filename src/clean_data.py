from pathlib import Path

import pandas as pd


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# Create a reusable cleaning function
def clean_property_data(df, year):

    print(f"\nCleaning {year} data...")

    # Check the raw dataset
    print("Starting shape:", df.shape)

    # Remove completely blank rows
    df = df.dropna(how="all").copy()
        # Standardize older column names
    column_renames = {
        "Taxkey": "taxkey",
        "Nbhd": "nbhd",
        "Nr_of_rms": "Rooms",
        "Fin_sqft": "FinishedSqft"
    }

    df = df.rename(columns=column_renames)

    # Add PropertyID if an older dataset does not contain it
    if "PropertyID" not in df.columns:
        df["PropertyID"] = pd.NA

    # Keep the original Sale_price values for validation
    raw_sale_price = df["Sale_price"].copy()
    raw_sale_date = df["Sale_date"].copy()

    print("Shape after removing blank rows:", df.shape)

    # Convert Sale_date into a true date
    df["Sale_date"] = pd.to_datetime(
        df["Sale_date"],
        errors="coerce"
    )

        # Check whether missing prices came from the source
    source_missing_prices = raw_sale_price.isna().sum()

    # Check whether cleaning caused any price conversion failures
    failed_price_conversions = (
        df["Sale_price"].isna()
        & raw_sale_price.notna()
    ).sum()

    print(
        "Sale_price values missing in source:",
        source_missing_prices
    )

    print(
        "Sale_price conversion failures:",
        failed_price_conversions
    )

    # Clean Sale_price formatting
    df["Sale_price"] = (
        df["Sale_price"]
        .astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    # Convert Sale_price into numeric data
    df["Sale_price"] = pd.to_numeric(
        df["Sale_price"],
        errors="coerce"
    )

    # Columns that should contain whole numbers
    integer_columns = [
        "PropertyID",
        "taxkey",
        "District",
        "nbhd",
        "Year_Built",
        "Rooms",
        "FinishedSqft",
        "Units",
        "Bdrms",
        "Fbath",
        "Hbath",
        "Lotsize"
    ]

    # Convert whole-number columns to nullable integers
    for column in integer_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("Int64")

    # Add SoldAsVacantLand for older datasets if it does not exist
    if "SoldAsVacantLand" not in df.columns:
        df["SoldAsVacantLand"] = pd.NA

    # Text columns that need whitespace cleaned
    text_columns = [
        "PropType",
        "Address",
        "CondoProject",
        "Style",
        "Extwall",
        "SoldAsVacantLand"
    ]

    # Remove extra spaces from text
    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Standardize Y/N capitalization
    if "SoldAsVacantLand" in df.columns:
        df["SoldAsVacantLand"] = (
            df["SoldAsVacantLand"].str.upper()
        )

        # Check exact duplicate records
    duplicate_count = df.duplicated().sum()

    print("Exact duplicate records:", duplicate_count)

    # Show duplicate records before removing them
    if duplicate_count > 0:
        duplicate_rows = df[df.duplicated(keep=False)]

        print("\nDuplicate rows before removal:")
        print(duplicate_rows.to_string(index=False))

    # Remove exact duplicate records
    df = df.drop_duplicates().copy()

    print("Exact duplicates removed:", duplicate_count)
    print("Shape after removing duplicates:", df.shape)

    # Check repeated PropertyID values
        # Check repeated PropertyID values when available
    if df["PropertyID"].notna().any():

        repeated_property_ids = (
            df["PropertyID"]
            .duplicated(keep=False)
            .sum()
        )

        print(
            "Rows with repeated PropertyID values:",
            repeated_property_ids
        )

    else:
        print(
            "Rows with repeated PropertyID values:",
            "Not available - no PropertyID in source"
        )

    # Add the sale year
    df["SaleYear"] = year

        # Flag records where Sale_date does not match the source dataset year
    df["YearMismatch"] = (
        df["Sale_date"].dt.year != year
    )

    # Final validation
    print(
        "Missing Sale_date values:",
        df["Sale_date"].isna().sum()
    )
        # Check whether Sale_date matches the dataset year
    year_mismatch = (
        df["Sale_date"].notna()
        & (df["Sale_date"].dt.year != year)
    )

    print(
        "Sale_date year mismatches:",
        year_mismatch.sum()
    )

    if year_mismatch.sum() > 0:
            print("\nRows where Sale_date does not match file year:")

            mismatch_rows = df.loc[
            year_mismatch,
            ["PropertyID", "Address", "Sale_date"]
            ].copy()

            mismatch_rows["Original_Sale_date"] = raw_sale_date.loc[
                mismatch_rows.index
            ]

            print(mismatch_rows.to_string(index=False))

    print(
        "Missing Sale_price values:",
        df["Sale_price"].isna().sum()
    )

    # Show records with missing Sale_price values
    missing_price_rows = df[df["Sale_price"].isna()]

    if len(missing_price_rows) > 0:
        print("\nRows with missing Sale_price:")
        print(missing_price_rows.to_string(index=False))
    print("Final dataset shape:", df.shape)

    # Give the cleaned dataset back
    return df

# -----------------------------
# CLEAN MULTIPLE YEARS
# -----------------------------

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

for year in years:

    # Path to the raw dataset
    file_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / f"milwaukee property sales {year}.csv"
    )

    # Load the raw dataset
    df = pd.read_csv(file_path)

    # Clean the dataset
    df = clean_property_data(
        df,
        year
    )

    # Path where the cleaned dataset will be saved
    output_file_path = (
        PROJECT_ROOT
        / "data"
        / "cleaned"
        / f"milwaukee_property_sales_{year}.csv"
    )

    # Save the cleaned dataset
    df.to_csv(
        output_file_path,
        index=False
    )

    print(f"Cleaned {year} dataset saved successfully.")
    print("Saved to:", output_file_path)