from pathlib import Path
import pandas as pd

# Find the main project folder 
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Years that will be combined
years = [
    2017, 
    2018, 
    2019, 
    2020, 
    2021, 
    2022, 
    2023, 
    2024, 
    2025]

print('Ready to combine datasets for:')
print(years)
cleaned_datasets = []

for year in years:
    # Path to the cleaned dataset
    file_path = (
        PROJECT_ROOT
        / "data"
        / "cleaned"
        / f"milwaukee_property_sales_{year}.csv"
    )

    # Load the cleaned dataset
    df = pd.read_csv(file_path)

    # Append the cleaned dataset to the list
    cleaned_datasets.append(df)

    print(
        f'{year}:',
        df.shape
    )

# Combine all cleaned yearly datasets
master_df = pd.concat(
    cleaned_datasets,
    ignore_index=True
)

print("\nCombined dataset shape:")
print(master_df.shape)

# Check how many records came from each source year
print("\nRecords by SaleYear:")
print(
    master_df["SaleYear"]
    .value_counts()
    .sort_index()
)

# Save the combined master dataset
output_file_path = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2017_2025.csv"
)

master_df.to_csv(
    output_file_path,
    index=False
)

print("\nMaster dataset saved successfully.")
print("Saved to:", output_file_path)