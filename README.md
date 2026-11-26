# Customer Churn / Sales Trend Analysis — E-commerce Analytics

An end-to-end data analysis project that explores simulated e-commerce orders to identify monthly revenue trends, top-performing product categories, and high-value customers, then presents practical business recommendations.

## Features
- Reproducible generator for a simulated e-commerce orders dataset
- Data quality checks for shape, data types, missing values, and duplicates
- Date feature engineering for month, weekday, and quarter
- Monthly revenue and month-over-month growth analysis
- Category performance analysis using `groupby` and `pivot_table`
- Customer spending analysis and top-10% revenue contribution (Pareto-style)
- Dashboard with monthly trends, category comparisons, and customer concentration
- One-page business brief with findings, recommendations, and next steps

## Tech stack
Python, NumPy, pandas, Matplotlib, Seaborn, Jupyter Notebook

## Run locally

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and run the analysis:

```bash
pip install -r requirements.txt
jupyter notebook sales_trend_analysis.ipynb
```

You can also run the Python script:

```bash
python sales_trend_analysis.py
```

The notebook and script use `ecommerce_orders.csv` included in this repository. The script can generate the dataset if the CSV is missing.

## Analysis details
- Dataset: simulated e-commerce orders (2,000 orders, 300 possible customer IDs, 4 product categories)
- Date range: January–December 2025
- Revenue field: order amount in USD
- Analysis: monthly revenue, month-over-month growth, category totals/averages/order counts, monthly category pivot, customer spend ranking
- Customer concentration: revenue share contributed by the top 10% of customers
- Outputs: dashboard PNG, business brief (PDF and Markdown), and analysis CSV tables

## Business brief
The one-page business brief is available as `business_brief.pdf` and `business_brief.md`. It uses the headings **Context**, **Key findings**, **Recommendations**, and **Next steps**.

## Project note
The dataset is generated and simulated for learning purposes. It does not contain real customer information, and the findings should not be interpreted as actual business performance. Recommendations are hypotheses to validate using real, permissioned sales data.
