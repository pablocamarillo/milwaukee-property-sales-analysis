from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt


# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Path to the master cleaned dataset
file_path = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "milwaukee_property_sales_2017_2025.csv"
)

# Load the master dataset
df = pd.read_csv(
    file_path,
    parse_dates=["Sale_date"]
)

print("Master dataset loaded successfully.")
print("Shape:", df.shape)

print("\nColumn names and data types:")
print(df.dtypes)

print("\nMissing values by column:")
print(
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

print("\nSale price summary:")
print(df["Sale_price"].describe())

print(
    "\nMedian sale price:",
    df["Sale_price"].median()
)

# Check for zero-dollar sales
zero_price_sales = (
    df["Sale_price"] == 0
).sum()

print(
    "\nZero-dollar sales:",
    zero_price_sales
)

# Show zero-dollar sale records
zero_price_rows = df[
    df["Sale_price"] == 0
]

print("\nZero-dollar sale records:")
print(
    zero_price_rows[
        [
            "SaleYear",
            "Sale_date",
            "PropType",
            "Address",
            "Sale_price"
        ]
    ].to_string(index=False)
)

# Inspect identifiers for zero-dollar sales
print("\nZero-dollar sale identifiers:")
print(
    zero_price_rows[
        [
            "SaleYear",
            "Sale_date",
            "PropertyID",
            "taxkey",
            "PropType",
            "Address",
            "Sale_price"
        ]
    ].to_string(index=False)
)

# Inspect repeated zero-dollar records in full
repeated_zero_sales = zero_price_rows[
    zero_price_rows["PropertyID"].isin(
        [137389, 137976]
    )
]

print("\nRepeated zero-dollar records - all columns:")
print(
    repeated_zero_sales.to_string(index=False)
)

# Keep only records with a positive sale price for price analysis
positive_price_sales = df[
    df["Sale_price"] > 0
].copy()

print("\nPositive-price sales:")
print(positive_price_sales.shape)

print("\nPositive sale price summary:")
print(
    positive_price_sales["Sale_price"].describe()
)

print(
    "\nPositive-price median:",
    positive_price_sales["Sale_price"].median()
)

# Check for very low-price sales
low_price_sales = positive_price_sales[
    positive_price_sales["Sale_price"] <= 1000
]

print(
    "\nSales for $1,000 or less:",
    len(low_price_sales)
)

# Show very low-price sale records
print("\nSales for $1,000 or less:")
print(
    low_price_sales[
        [
            "SaleYear",
            "Sale_date",
            "PropType",
            "Address",
            "Sale_price"
        ]
    ].sort_values("Sale_price").to_string(index=False)
)

# Calculate median sale price by year
median_price_by_year = (
    positive_price_sales
    .groupby("SaleYear")["Sale_price"]
    .median()
)

print("\nMedian sale price by year:")
print(median_price_by_year)

# Calculate yearly percentage change in median sale price
median_price_change = (
    median_price_by_year
    .pct_change() * 100
)

print("\nYear-over-year change in median sale price:")
print(
    median_price_change.round(2)
)

# Count property sales by year
sales_by_year = (
    positive_price_sales
    .groupby("SaleYear")
    .size()
)

print("\nNumber of positive-price sales by year:")
print(sales_by_year)

# Calculate yearly percentage change in sales volume
sales_volume_change = (
    sales_by_year
    .pct_change() * 100
)

print("\nYear-over-year change in sales volume:")
print(
    sales_volume_change.round(2)
)

# Combine yearly price and volume metrics
yearly_summary = pd.DataFrame({
    "MedianSalePrice": median_price_by_year,
    "MedianPriceChangePct": median_price_change,
    "SalesVolume": sales_by_year,
    "SalesVolumeChangePct": sales_volume_change
})

print("\nYearly market summary:")
print(
    yearly_summary.round(2)
)

# Plot median sale price by year
plt.plot(
    median_price_by_year.index,
    median_price_by_year.values,
    marker="o"
)

plt.title("Milwaukee Median Property Sale Price, 2017-2025")
plt.xlabel("Year")
plt.ylabel("Median Sale Price ($)")

plt.grid(True)
plt.tight_layout()

plt.show()

# Plot number of sales by year
plt.plot(
    sales_by_year.index,
    sales_by_year.values,
    marker="o"
)

plt.title("Milwaukee Property Sales Volume, 2017-2025")
plt.xlabel("Year")
plt.ylabel("Number of Sales")

plt.grid(True)
plt.tight_layout()

plt.show()

# Count sales by property type
property_type_counts = (
    positive_price_sales["PropType"]
    .value_counts()
)

print("\nSales by property type:")
print(property_type_counts)

# Calculate percentage of sales by property type
property_type_percent = (
    positive_price_sales["PropType"]
    .value_counts(
        normalize=True,
        dropna=False
    ) * 100
)

print("\nPercentage of sales by property type:")
print(
    property_type_percent.round(2)
)

# Calculate median sale price by property type
median_price_by_type = (
    positive_price_sales
    .groupby("PropType")["Sale_price"]
    .median()
    .sort_values(ascending=False)
)

print("\nMedian sale price by property type:")
print(median_price_by_type)

# Compare mean and median sale prices by property type
price_summary_by_type = (
    positive_price_sales
    .groupby("PropType")["Sale_price"]
    .agg(["count", "mean", "median"])
    .sort_values("median", ascending=False)
)

print("\nPrice summary by property type:")
print(
    price_summary_by_type.round(2)
)

# Create a residential-only dataset
residential_sales = positive_price_sales[
    positive_price_sales["PropType"] == "Residential"
].copy()

print("\nResidential sales:")
print(residential_sales.shape)

print("\nResidential median sale price by year:")
print(
    residential_sales
    .groupby("SaleYear")["Sale_price"]
    .median()
)

# Calculate residential median sale price by year
residential_median_by_year = (
    residential_sales
    .groupby("SaleYear")["Sale_price"]
    .median()
)

# Calculate yearly percentage change
residential_price_change = (
    residential_median_by_year
    .pct_change() * 100
)

print("\nYear-over-year change in residential median price:")
print(
    residential_price_change.round(2)
)

# Count unique residential neighborhoods
unique_neighborhoods = (
    residential_sales["nbhd"]
    .nunique()
)

print(
    "\nNumber of residential neighborhoods:",
    unique_neighborhoods
)

# Find the 10 neighborhoods with the most residential sales
top_neighborhoods_by_sales = (
    residential_sales["nbhd"]
    .value_counts()
    .head(10)
)

# Get the neighborhood codes from the top 10 by sales volume
top_neighborhood_codes = top_neighborhoods_by_sales.index

# Calculate median sale price for those neighborhoods
top_neighborhood_prices = (
    residential_sales[
        residential_sales["nbhd"].isin(top_neighborhood_codes)
    ]
    .groupby("nbhd")["Sale_price"]
    .median()
    .sort_values(ascending=False)
)

print("\nMedian sale price for top 10 high-volume neighborhoods:")
print(top_neighborhood_prices)

print("\nTop 10 residential neighborhoods by sales volume:")
print(top_neighborhoods_by_sales)

# Combine sales volume and median price for top neighborhoods
top_neighborhood_summary = pd.DataFrame({
    "SalesVolume": top_neighborhoods_by_sales,
    "MedianSalePrice": top_neighborhood_prices
})

print("\nTop neighborhood summary:")
print(
    top_neighborhood_summary
    .sort_values("SalesVolume", ascending=False)
)

neighborhood_area_map = {
    2100.0: "West Side/Mount Mary",
    2080.0: "West Side/Mount Mary",
    4520.0: "Wilson Park",
    4240.0: "Fairview",
    4420.0: "Alverno",
    4340.0: "Euclid Park",
    1140.0: "Havenwoods/Thurston Woods",
    4120.0: "South Side",
    4620.0: "Bay View",
    2040.0: "West Side/Mount Mary"
}

top_neighborhood_summary["ResidentialArea"] = (
    top_neighborhood_summary.index.map(neighborhood_area_map)
)

# Create readable neighborhood labels
top_neighborhood_summary["NeighborhoodLabel"] = (
    top_neighborhood_summary.index.astype(int).astype(str)
    + " - "
    + top_neighborhood_summary["ResidentialArea"]
)

print("\nNeighborhood labels:")
print(
    top_neighborhood_summary[
        ["NeighborhoodLabel", "SalesVolume", "MedianSalePrice"]
    ]
    .sort_values("SalesVolume", ascending=False)
)

# Plot median sale price for top 10 high-volume neighborhoods
neighborhood_price_chart = (
    top_neighborhood_summary
    .sort_values("MedianSalePrice", ascending=True)
    .copy()
)

# Give each neighborhood its own numeric position
y_positions = range(len(neighborhood_price_chart))

# Create a larger figure
plt.figure(figsize=(12, 7))

# Create horizontal bars
plt.barh(
    y_positions,
    neighborhood_price_chart["MedianSalePrice"].values
)

# Replace numeric positions with neighborhood names
plt.yticks(
    y_positions,
    neighborhood_price_chart["NeighborhoodLabel"].tolist()
)

plt.title(
    "Median Residential Sale Price in Top 10 High-Volume Neighborhoods"
)
plt.xlabel("Median Sale Price ($)")
plt.ylabel("Neighborhood")

plt.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()
plt.show()

# Plot residential median sale price by year
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    residential_median_by_year.index,
    residential_median_by_year.values,
    marker="o"
)

ax.set_title(
    "Milwaukee Residential Median Sale Price, 2017-2025"
)
ax.set_xlabel("Year")
ax.set_ylabel("Median Sale Price ($)")

ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()