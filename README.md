# DataCo-Smart-Supply-Chain-Analytics-Diagnostics

An end-to-end analysis of the DataCo Smart Supply Chain dataset (180,519 order
lines, 2015 to early 2018, about $36.8M in sales) to understand where revenue
comes from, whether it is profitable, and where delivery and fraud risks sit.

## What this project does
- **Data cleaning (Python/pandas):** quality checks, removed 5 uninformative
  columns, converted dates.
- **Feature engineering:** order year/month/quarter, shipping duration,
  weekend orders, sales and profit categories, profit margin, shipping
  performance.
- **EDA:** 23 business questions across sales, products, geography, customers,
  logistics, and fraud, each with an insight and recommendation.
- **SQL (MySQL):** one query per business question, plus a Python script that
  exports all results to a single Excel workbook.
- **Dashboard:** interactive view with filters by year, market, segment,
  shipping mode, department, delivery status, and order status, and a
  switchable metric and breakdown.

## Key findings
- The top 10 product categories generate about 90% of sales.
- About 19% of order lines are loss-making, offsetting roughly half of the
  profit earned on profitable lines.
- 54.8% of deliveries are late. The rate is similar across markets and
  customer segments but varies sharply by shipping mode (Standard 38%,
  Second Class 77%, First Class 95%).
- Suspected fraud is about 2.25% of lines and roughly uniform across markets.

## Tech stack
Python (pandas, NumPy, Matplotlib, Seaborn), MySQL, SQLAlchemy, openpyxl,
HTML/JavaScript dashboard.

## Data
[DataCo Smart Supply Chain for Big Data Analysis](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) (Kaggle).
