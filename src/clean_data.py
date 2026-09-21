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

    print("Shape after removing blank rows:", df.shape)

    # Convert Sale_date into a true date
    df["Sale_date"] = pd.to_datetime(
        df["Sale_date"],
        errors="coerce"
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

    # Check exact duplicates
    duplicate_count = df.duplicated().sum()

    print("Exact duplicate records:", duplicate_count)

    # Check repeated PropertyIDs
    repeated_property_ids = (
        df["PropertyID"]
        .duplicated(keep=False)
        .sum()
    )

    print(
        "Rows with repeated PropertyID values:",
        repeated_property_ids
    )

    # Add the year as its own column
    df["SaleYear"] = year

    # Final validation
    print("Missing Sale_date values:", df["Sale_date"].isna().sum())
    print("Missing Sale_price values:", df["Sale_price"].isna().sum())
    print("Final dataset shape:", df.shape)

    # Give the cleaned dataset back
    return df


# -----------------------------
# CLEAN 2025 DATA
# -----------------------------

# Path to the raw 2025 file
file_path = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "milwaukee property sales 2025.csv"
)

# Load the raw CSV
df_2025 = pd.read_csv(file_path)

# Send the dataset through our cleaning function
df_2025 = clean_property_data(
    df_2025,
    2025
)

# Path where the cleaned file will be saved
output_file_path = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2025.csv"
)

# Save the cleaned dataset
df_2025.to_csv(
    output_file_path,
    index=False
)

print("\nCleaned 2025 dataset saved successfully.")
print("Saved to:", output_file_path)

# -----------------------------
# CLEAN 2024 DATA
# -----------------------------

# Path to the raw 2024 file
file_path_2024 = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "milwaukee property sales 2024.csv"
)

# Load the raw 2024 CSV
df_2024 = pd.read_csv(file_path_2024)

# Send 2024 through the SAME cleaning function
df_2024 = clean_property_data(
    df_2024,
    2024
)

# Path where the cleaned 2024 file will be saved
output_file_path_2024 = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2024.csv"
)

# Save the cleaned 2024 dataset
df_2024.to_csv(
    output_file_path_2024,
    index=False
)

print("\nCleaned 2024 dataset saved successfully.")
print("Saved to:", output_file_path_2024)

# -----------------------------
# CLEAN 2023 DATA
# -----------------------------

# Path to the raw 2023 file
file_path_2023 = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "milwaukee property sales 2023.csv"
)

# Load the raw 2023 CSV
df_2023 = pd.read_csv(file_path_2023)

# Send 2023 through the SAME cleaning function
df_2023 = clean_property_data(
    df_2023,
    2023
)

# Path where the cleaned 2023 file will be saved
output_file_path_2023 = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2023.csv"
)

# Save the cleaned 2023 dataset
df_2023.to_csv(
    output_file_path_2023,
    index=False
)

print("\nCleaned 2023 dataset saved successfully.")
print("Saved to:", output_file_path_2023)

# -----------------------------
# CLEAN 2022 DATA
# -----------------------------

# Path to the raw 2022 file
file_path_2022 = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "milwaukee property sales 2022.csv"
)

# Load the raw 2022 CSV
df_2022 = pd.read_csv(file_path_2022)

# Send 2022 through the SAME cleaning function
df_2022 = clean_property_data(
    df_2022,
    2022
)

# Path where the cleaned 2022 file will be saved
output_file_path_2022 = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2022.csv"
)

# Save the cleaned 2022 dataset
df_2022.to_csv(
    output_file_path_2022,
    index=False
)

print("\nCleaned 2022 dataset saved successfully.")
print("Saved to:", output_file_path_2022)