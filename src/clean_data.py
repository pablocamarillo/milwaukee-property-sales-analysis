# Milwaukee Property Sales Data Cleaning Script
# Cleans and standardizes Milwaukee property sales data from 2017-2025.
from pathlib import Path
import pandas as pd 
# find the project root folder 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Path to the raw 2025 dataset
file_path = (
    PROJECT_ROOT
    /"data"
    /"raw"
    /"milwaukee property sales 2025.csv"
)
# Load the dataset
df = pd.read_csv(file_path)
# Check the dataset before cleaning 
print("Before cleaning:")
print("Rows and columns:", df.shape)
# Reomve rows where every column is blank
df = df.dropna(how='all')
# Check the dataset after removing blank rows
print("\nAfter removing completely blank rows:")
print("Rows and columns:", df.shape)
# Check missing values after removing blank rows
print("\nMissing values by column:")
print(df.isna().sum())
# Check the data type of each column
print("\nData types:")
print(df.dtypes)
# Convert Sale_date from text to a true datetime
df["Sale_date"] = pd.to_datetime(df["Sale_date"], errors="coerce")
# Verify the Sale_date conversion
print("\nSale_date data type after conversion:")
print(df["Sale_date"].dtype)
print("\nMissing Sale_date values after conversion:")
print(df["Sale_date"].isna().sum())
# Convert Sale_price to numeric
df["Sale_price"] = pd.to_numeric(df["Sale_price"], errors="coerce")
# Verify the Sale_price conversion
print("\nSale_price data type after conversion:")
print(df["Sale_price"].dtype)
print("\nMissing Sale_price values after conversion:")
print(df["Sale_price"].isna().sum())
print("\nSale_price range:")
print("Min:", df["Sale_price"].min())
print("Max:", df["Sale_price"].max())
# Convert whole-number columns to nullable integers
integer_columns = ["PropertyID", "taxkey", "District", "nbhd", "Year_Built", "Rooms", "FinishedSqft", "Units", "Bdrms", "Fbath", "Hbath", "Lotsize"]
for column in integer_columns:
    df[column] = df[column].astype("Int64")
# Verify the new data types
print("\nData types after integer conversion:")
print(df[integer_columns].dtypes)
# Clean whitespace from text columns
text_columns = ["PropType", "Address", "CondoProject", "Style", "Extwall", "SoldAsVacantLand"]
for column in text_columns:
    df[column] = df[column].str.strip()
# Standardize SoldAsVacantLand capitalization
df["SoldAsVacantLand"] = df["SoldAsVacantLand"].str.upper()
# Verify important categorical values
print("\nProperty types:")
print(df["PropType"].value_counts())
print("\nSoldAsVacantLand values:")
print(df["SoldAsVacantLand"].value_counts(dropna=False))
# Check for exact duplicate records after cleaning
duplicate_count = df.duplicated().sum()
print("\nExact duplicate records after cleaning:")
print(duplicate_count)
# Check for PropertyID values that appear more than once
repeated_property_ids = df["PropertyID"].duplicated(keep=False).sum()
print("\nPropertyIDs that appear more than once:")
print(repeated_property_ids)
# Add the sale year for easier multi-year analysis
df["SaleYear"] = 2025
# Verify the new column
print("\nSaleYear values:")
print(df["SaleYear"].value_counts())
print("\nFinal dataset shape:")
print(df.shape)
# Path for the cleaned 2025 dataset
output_file_path = (
    PROJECT_ROOT / "data" / "cleaned" / "milwaukee_property_sales_2025.csv"
)
# Save the cleaned dataset
df.to_csv(output_file_path, index=False)
print("\nCleaned 2025 dataset saved successfully.")
print("Saved to:", output_file_path)