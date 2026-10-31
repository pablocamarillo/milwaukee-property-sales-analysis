# Milwaukee Property Sales Analysis (2017–2025)

A Python-based exploratory analysis of historical Milwaukee real estate transactions, supported by an Excel data audit.

**53,607 cleaned records · 9 source years · Python, Pandas, Matplotlib, Excel**

[Overview](#project-overview) · [Dataset](#dataset-overview) · [Findings](#key-findings) · [Visualizations](#visualizations) · [Run the project](#getting-started) · [Status](#project-status)

## Project Overview

This project examines how recorded Milwaukee property sales differ across years, property types, and neighborhood codes. It combines yearly files into a consistent dataset, investigates data quality, and uses descriptive statistics to explore residential prices and transaction activity.

Milwaukee's mix of residential, condominium, apartment, and commercial sales makes it useful for studying how the population being analyzed affects the results. The analysis asks:

- How did residential median sale prices and transaction counts change across source years?
- How do sale-price distributions differ by property type?
- Which neighborhood codes have the most residential sales, and how do their median prices compare?
- Which missing values, unusual transactions, and date inconsistencies need additional review?

Python and Pandas handle cleaning and analysis. Matplotlib displays the results, while Excel supports file inventory and cross-year column review. The work demonstrates a progression from inspecting real-world data to documenting reproducible descriptive findings.

## Project Objectives

| Objective | Current implementation |
| --- | --- |
| Clean and validate transaction data | Standardizes yearly columns and types, removes blank rows and exact duplicates, and reports quality checks. |
| Explore sale prices and unusual transactions | Calculates descriptive statistics and inspects zero-price and very low-price records. |
| Compare years and property types | Produces annual medians, transaction counts, percentage changes, and property-type summaries. |
| Examine neighborhood patterns | Compares residential volume and median prices for the ten highest-volume neighborhood codes. |
| Communicate findings visually | Four chart sections are implemented; exported portfolio images and final captions are planned. |
| Resolve remaining interpretation questions | Source attribution, date anomalies, neighborhood-label validation, and distribution graphics remain in progress. |

## Dataset Overview

The repository contains **nine raw yearly CSVs**, **nine cleaned yearly CSVs**, and one combined cleaned dataset.

| Measure | Verified value |
| --- | ---: |
| Source-file years | 2017–2025 |
| Combined cleaned records | 53,607 |
| Combined columns | 23 |
| Positive-price records used for price analysis | 53,590 |
| Positive-price residential records | 42,688 |
| Missing sale prices | 10 |
| Zero-price transactions | 7 |
| Source-year/date mismatches | 6 |

Important fields include `Sale_price`, `Sale_date`, `SaleYear`, `PropType`, `nbhd`, `District`, `taxkey`, `PropertyID`, `FinishedSqft`, `Year_Built`, and `YearMismatch`. `SaleYear` records the **source-file year**, which is the grouping used by the existing analysis.

Recorded property categories are Residential, Condominium, Lg Apartment, Commercial, Vacant Land, Manufacturing, and Exempt. Eight records have a missing property category.

**Coverage and provenance:** 2017–2025 describes the source files, not a guarantee that every recorded transaction date lies in that interval. Six records in the 2019 file have later dates, including one in 2028. The repository does not yet document the original download URLs, retrieval dates, or dataset reuse terms. These remain to be confirmed; no source attribution or license is assumed.

**Data quality:** Older files use different column names and have less date precision. Some fields were not present in every year. The combined data includes substantial missingness in fields such as `CondoProject`, `SoldAsVacantLand`, and `PropertyID`; missing values should be interpreted in that context.

See [Analysis Notes](docs/analysis-notes.md) for yearly counts, filters, quality checks, and limitations.

## Technologies Used

| Technology | Role in this repository |
| --- | --- |
| Python | Runs the data preparation and analysis scripts. |
| Pandas | Loads CSVs, standardizes fields, combines years, and calculates descriptive summaries. |
| Matplotlib | Creates annual trend and neighborhood-comparison charts. |
| Microsoft Excel | Supports the file inventory and cross-year column audit in the existing workbook. |

The scripts were tested with **Python 3.13.15, Pandas 2.3.3, and Matplotlib 3.10.6**. Direct Python dependencies are recorded in [requirements.txt](requirements.txt). No Jupyter notebooks are currently included.

## What This Project Can Do

- Load the yearly property-sales CSVs and inspect their structure.
- Standardize older column names, parse dates and prices, normalize selected text fields, and prepare a common schema.
- Remove completely blank rows and exact duplicates while retaining repeated identifiers for review.
- Combine cleaned yearly files into one dataset with source-year and date-mismatch fields.
- Calculate counts, mean and median prices, descriptive summaries, and year-over-year changes.
- Compare property categories and positive-price residential sales across source years.
- Display annual median-price and sales-volume charts, plus a residential neighborhood comparison.

## Key Findings

These results were verified from the existing combined dataset on **October 31, 2026**, using the filters already implemented in the analysis script. They describe recorded sales, not changes in the value of every property.

| Finding | Evidence and scope |
| --- | --- |
| Residential median sale prices were higher in 2025 than in 2017. | Among positive-price Residential records, the median rose from **$135,000** to **$235,000**, a **74.1% nominal increase** across source years. |
| Residential transaction activity peaked in source year 2022. | The positive-price residential subset contains **5,774** records for 2022 and **4,530** for 2025, a **21.5% decrease** from that peak. |
| Price analysis excludes a small set of unusable prices. | **10 missing prices and 7 zero-price records** are excluded by `Sale_price > 0`, leaving **53,590** records across all property types. |

The results are not inflation-adjusted or adjusted for changes in the mix of properties sold. Date anomalies remain in their source-year groups. Neighborhood labels in the script are manually assigned and need validation before geographic conclusions are finalized.

## Visualizations

**Chart code is implemented; finalized image exports are planned.** Running [analyze_data.py](src/analyze_data.py) displays:

1. Median positive property sale price by source year, 2017–2025.
2. Positive-price transaction volume by source year.
3. Median residential sale prices for the ten highest-volume neighborhood codes.
4. Median positive residential sale price by source year.

No saved chart images are currently included, so this README does not show placeholder images or claim a finished dashboard. Next steps are to review chart behavior, validate neighborhood labels, and export selected figures with concise captions. See the [plotting notes](docs/analysis-notes.md#visualization-review) before preparing portfolio screenshots.

## Repository Structure

```text
milwaukee-property-sales-analysis/
├── README.md
├── requirements.txt
├── .gitattributes
├── .gitignore
├── data/
│   ├── raw/                # Nine yearly CSVs and README.md.txt
│   └── cleaned/            # Nine yearly CSVs, combined CSV, and README.md.txt
├── docs/
│   └── analysis-notes.md
├── excel/
│   └── milwaukee_property_sales_data_audit.xlsx
├── reasearch/
│   ├── cleaning_log.md
│   ├── project_questions.md
│   └── research__notes.md.txt
└── src/
    ├── clean_data.py
    ├── combine_data.py
    └── analyze_data.py
```

The existing `reasearch` spelling is preserved to avoid unnecessary path changes. An empty local `dashboard/` directory is not tracked by Git and is not part of the clone. Figures and notebook folders will be added only when those artifacts exist.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pablocamarillo/milwaukee-property-sales-analysis.git
cd milwaukee-property-sales-analysis
```

Repository access is required if it is private.

### 2. Set up Python dependencies

Use Python 3.13 for the tested setup. In Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS or Linux, use `python3 -m venv .venv` and `.venv/bin/python` in place of the Windows interpreter path below. Those platforms have not been tested for this project.

### 3. Locate the data

Original yearly files are in [data/raw](data/raw). Prepared files are in [data/cleaned](data/cleaned), including:

```text
data/cleaned/milwaukee_property_sales_2017_2025.csv
```

The existing analysis can run directly against that combined dataset.

### 4. Run the analysis

```powershell
.\.venv\Scripts\python.exe src/analyze_data.py
```

The script prints descriptive summaries and opens Matplotlib charts. With a blocking desktop backend, close each chart window to continue. A noninteractive run can be used to check execution without opening windows:

```powershell
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe src/analyze_data.py
Remove-Item Env:MPLBACKEND
```

The noninteractive run does not export images. Use a separate PowerShell session for this check if you already have a custom plotting-backend setting.

### 5. Review the Excel audit

Open [milwaukee_property_sales_data_audit.xlsx](excel/milwaukee_property_sales_data_audit.xlsx) in Microsoft Excel. Its File Inventory and Column Comparison worksheets document the initial file review. The workbook is an audit artifact; it is not a completed chart dashboard.

### Optional: rebuild prepared data

Run preparation only when you intend to regenerate the outputs:

```powershell
.\.venv\Scripts\python.exe src/clean_data.py
.\.venv\Scripts\python.exe src/combine_data.py
```

These commands overwrite yearly cleaned files and the combined CSV respectively. Preserve any modified outputs first. The raw files are inputs and should remain unchanged.

## Project Status

| Status | Work |
| --- | --- |
| Completed | Yearly data inspection, Excel inventory, reusable preparation scripts, combined dataset, descriptive analysis, and chart-generating code. |
| In progress | Interpretation of findings, validation of neighborhood labels and date anomalies, and portfolio documentation. |
| Planned | Final figure exports and captions, distribution plots, confirmed source/reuse documentation, and clearer post-conversion validation diagnostics. |

Existing scripts, research history, workbook contents, and datasets are preserved. Preparation and analysis execution have been checked in an isolated copy; a fresh dependency installation and a visual review of every chart remain separate checks. The [analysis notes](docs/analysis-notes.md) describe current limitations without changing the original results.

## Skills Demonstrated

- **Python programming:** reusable cleaning logic and project-relative file handling.
- **Pandas data manipulation:** type conversion, concatenation, filtering, grouping, and aggregation.
- **Data cleaning and validation:** schema comparison, missing-value checks, duplicate review, and date-quality flags.
- **EDA and descriptive statistics:** population-specific comparisons, summary statistics, and transaction-pattern exploration.
- **Matplotlib visualization:** line charts and horizontal bar-chart code.
- **Excel data review:** workbook-based file inventory and column comparison.
- **Analytical problem-solving and communication:** documented assumptions, research questions, and findings tied to explicit filters.

## Author

**Pablo Camarillo**

Data Analytics & Applied AI Student

[GitHub profile](https://github.com/pablocamarillo)
