# Analysis Notes

[Project overview](../README.md) · [Analysis script](../src/analyze_data.py) · [Original research questions](../reasearch/project_questions.md)

This document records the data and code audit performed on October 31, 2026. It supplements the original research files without replacing historical notes or changing analytical results.

## Data inventory and coverage

Nine source files cover 2017–2025. The raw CSVs contain **53,781 data rows** under Pandas' default CSV reading behavior, including **107 rows with all values missing**. After the existing preparation workflow, the combined dataset contains **53,607 rows and 23 columns**. Counts exclude the CSV header; physically empty lines skipped by Pandas are not counted.

| Source year | Raw data rows | All-missing rows | Cleaned rows | Positive-price residential rows | Residential median price |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2017 | 4,840 | 0 | 4,836 | 3,699 | $135,000 |
| 2018 | 5,515 | 0 | 5,512 | 4,206 | $139,900 |
| 2019 | 6,211 | 1 | 6,158 | 4,709 | $138,000 |
| 2020 | 6,355 | 1 | 6,354 | 5,254 | $160,000 |
| 2021 | 6,508 | 0 | 6,500 | 5,244 | $172,600 |
| 2022 | 7,146 | 0 | 7,146 | 5,774 | $186,950 |
| 2023 | 5,831 | 0 | 5,831 | 4,672 | $195,150 |
| 2024 | 5,690 | 0 | 5,690 | 4,600 | $220,000 |
| 2025 | 5,685 | 105 | 5,580 | 4,530 | $235,000 |
| **Total** | **53,781** | **107** | **53,607** | **42,688** | — |

The Excel inventory records 4,841 rows for 2017 and 5,516 for 2018; the parsed CSV data-row counts are 4,840 and 5,515. The one-row differences may reflect header counting, but that explanation is not verified. The workbook remains unchanged; use the explicit counting definition above for this document.

## Field guide

| Fields | Use and caution |
| --- | --- |
| `Sale_price` | Numeric transaction price; existing price analysis keeps values greater than zero. |
| `Sale_date` | Parsed transaction date; older month-only strings acquire a day during parsing and do not establish exact day-level precision. |
| `SaleYear` | Source-file year assigned by the cleaning script, not derived from `Sale_date`. |
| `YearMismatch` | Flags a difference between parsed date year and source-file year. |
| `PropType` | Recorded property category; Residential is the specific category used for the residential subset. |
| `nbhd`, `District` | Geographic codes; neighborhood labels in the script are a manual mapping requiring verification. |
| `taxkey`, `PropertyID` | Identifiers; repeated identifiers can represent separate transactions. `PropertyID` is not available across all source years. |
| `FinishedSqft`, `Lotsize`, `Year_Built`, `Rooms`, `Units` | Property attributes with varying completeness; their presence does not mean size-adjusted modeling has been completed. |

## Analytical populations

The analysis script uses:

```python
positive_price_sales = df[df["Sale_price"] > 0].copy()
residential_sales = positive_price_sales[
    positive_price_sales["PropType"] == "Residential"
].copy()
```

- Full combined dataset: **53,607** rows.
- Positive-price subset: **53,590** rows, excluding **10 missing prices** and **7 zero-price sales**. There are no negative prices in the audited file.
- Positive-price Residential subset: **42,688** rows. Condominium and Lg Apartment are separate recorded categories and are not included in this subset.
- Neighborhood comparisons select the ten `nbhd` codes with the most residential records across the full period, then calculate their median prices. They do not rank all neighborhoods by price growth or estimate neighborhood-level trends over time.

## Findings and calculations

Annual comparisons group on `SaleYear`. The current script retains date-mismatch records in their source-year groups.

- Residential median price: `(235000 / 135000 - 1) × 100 = 74.074…%` from source year 2017 to 2025, reported as **74.1%**.
- Positive-price residential volume: 2022 has the largest count, **5,774**; 2025 has **4,530**. `(4530 / 5774 - 1) × 100 = -21.544…%`, reported as a **21.5% decrease**.
- These are nominal, unadjusted comparisons of observed transactions. They are not causal estimates, a repeat-sales index, or an appraisal model.

Reproduce the residential annual table from the project root with the same Python environment used by the scripts:

```python
import pandas as pd

df = pd.read_csv(
    "data/cleaned/milwaukee_property_sales_2017_2025.csv",
    low_memory=False,
)
residential = df.loc[
    (df["Sale_price"] > 0) & (df["PropType"] == "Residential")
]
print(
    residential.groupby("SaleYear")["Sale_price"]
    .agg(SalesVolume="size", MedianSalePrice="median")
)
```

## Data quality and unresolved questions

1. **Date anomalies:** Six rows assigned to source year 2019 have dates in 2020, 2024, or 2028. The parsed date range is 2017-01-01 through 2028-06-13. No correction or exclusion was made during the documentation audit.
2. **Missing fields:** `PropType` is missing in 8 rows, `nbhd` in 57, `PropertyID` in 10,348, `SoldAsVacantLand` in 42,337, and `CondoProject` in 46,017. Some missingness reflects source schema and property-type differences. No imputation is claimed.
3. **Duplicates:** The combined dataset contains no exact duplicate rows under a full-row comparison. This does not establish that every economic transaction is unique; repeated property identifiers still need contextual interpretation.
4. **Validation diagnostic ordering:** In `clean_data.py`, the printed price-conversion-failure check currently runs before price conversion. It cannot establish the number of conversion failures. Moving or strengthening that diagnostic is a future code change; the existing script has been preserved.
5. **Mixed-type warning:** Reading the combined CSV with the current analysis script produces a Pandas `DtypeWarning` for `SoldAsVacantLand`. The run completes, but explicit import types merit review.
6. **Source and reuse documentation:** Download URLs, retrieval dates, and reuse terms are not recorded in the repository. Confirm them before representing the dataset as licensed for redistribution. No new data files were added in this cleanup.

## Visualization review

The existing script contains four `plt.show()` calls and no image-export calls. There are no saved figures in the repository at the time of this audit.

The first two chart sections reuse the current figure rather than creating separate figures. A blocking desktop session may close the first figure before the next chart is drawn; a headless or nonblocking session can instead retain the first plot. Review figure separation before exporting screenshots. No plotting code or analytical result was changed during this documentation task.

Planned presentation work: isolate each chart, validate the manual neighborhood labels, choose consistent formatting and captions, and save selected images to a `figures/` directory when actual exports are ready. Price-distribution graphics are also planned; no histogram is claimed as an existing output.

## Repository organization

Keep working paths in `data/`, `src/`, `excel/`, and `reasearch/` stable. `docs/` holds the current interpretation and audit notes. A future `figures/` folder should hold actual exported charts; create `notebooks/` only if interactive notebooks are added. Avoid creating empty scaffolding or renaming the research folder solely for appearance.

The existing `.gitignore` already excludes `.venv`, `.env`, bytecode, notebook checkpoints, and common tool caches. No data, workbook, or figure exclusions were added. Existing project files total approximately 23.1 MB before these documentation additions; no large data additions were made.

## Verification scope

- All original project files were inventoried with SHA-256 hashes and backed up outside the repository before changes.
- Existing Python files were parsed for syntax. The preparation and analysis workflows were exercised in a disposable copy; original data files were not regenerated.
- The Excel workbook was inspected read-only and its archive integrity checked. It contains file-inventory and column-comparison work, not a finished chart dashboard.
- README relative links, section anchors, and Markdown rendering were checked locally.
- Direct dependency versions match the tested environment. A clean online dependency installation, interactive Excel behavior, and a visual review of every Matplotlib chart were not part of this verification.
- Live GitHub access was unavailable during the audit. Publishing changes and confirming recruiter access remain separate steps.
