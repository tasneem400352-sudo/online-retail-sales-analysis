
# Online Retail Sales Analysis

## Project overview
An exploratory analysis of the UCI Online Retail dataset using Python. I examined monthly sales, cancellations, and sales by country and product.

## Tools
- Python
- pandas
- Matplotlib

## What I analyzed
- Checked the dataset structure and missing values.
- Calculated each line's value as quantity × unit price.
- Compared monthly sales before and after cancellations.
- Measured cancellation value as a percentage of sales.
- Summarized sales by country and ranked products, excluding postage and manual transaction codes from product rankings.

## Key findings
- The dataset contains 541,909 transaction rows.
- Monthly sales value peaked in November 2011 at approximately £1.51 million before cancellations.
- December 2011 is partial, so it should not be compared directly with full months.
- The cancellation percentage is based on transaction value, not the number of cancelled invoices.

## How to run
1. Download the Excel file from the UCI source below.
2. Put `Online Retail.xlsx` in the same folder as `online_retail_analysis.py`.
3. Run the Python file.

## Data source
[UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail) — CC BY 4.0.
