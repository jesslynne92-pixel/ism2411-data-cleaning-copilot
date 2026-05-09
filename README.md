# ism2411-data-cleaning-copilot

A data cleaning mini-project for ISM 2411. Cleans a messy raw sales CSV using Python and pandas, then exports a tidy processed file ready for analysis.

## What it does

- Standardizes column names (lowercase, underscores)
- Strips whitespace from product names and categories
- Fills or drops missing prices and quantities
- Removes rows with negative/zero prices or quantities
- Removes exact duplicate rows
- Exports a clean CSV to `data/processed/`

## How to run

1. Make sure Python and pandas are installed:
   ```
   pip install pandas
   ```

2. From the project root folder, run:
   ```
   python src/data_cleaning.py
   ```

3. The cleaned file will appear at `data/processed/sales_data_clean.csv`.

## Project structure

```
ism2411-data-cleaning-copilot/
├── data/
│   ├── raw/
│   │   └── sales_data_raw.csv
│   └── processed/
│       └── sales_data_clean.csv
├── src/
│   └── data_cleaning.py
├── README.md
└── reflection.md
```

## Tools used

- Python 3
- pandas
- GitHub Copilot (for initial function drafts)
