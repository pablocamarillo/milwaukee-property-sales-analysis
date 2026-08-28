## 2025 — Initial Validation

The initial data inspection documented:

- 5,685 total rows
- 21 columns
- 105 completely blank rows
- 0 true property-record duplicates

After loading the raw file into pandas, Python returned:

(5685, 21)

This matched the dimensions recorded during the initial inspection,
confirming that the raw dataset loaded correctly.

### Cleaning Step 1

Removed completely blank rows using:

df = df.dropna(how="all")

Result:

(5580, 21)

A total of 105 rows were removed, matching the number of completely
blank rows identified during the initial inspection.