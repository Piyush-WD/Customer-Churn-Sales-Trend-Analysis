"""
Project 03: Customer Churn / Sales Trend Analysis
This project follows the supplied guide's e-commerce sales analysis workflow.
The data is generated and simulated; it is not real customer data.
Run from the folder containing this script.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "ecommerce_orders.csv"
DASHBOARD_FILE = BASE / "sales_analysis_dashboard.png"

# Reproducible data generator (used if the CSV is missing).
if not DATA_FILE.exists():
    rng = np.random.default_rng(42)
    n = 2000
    orders = pd.DataFrame({
        "order_date": pd.to_datetime("2025-01-01") + pd.to_timedelta(
            rng.integers(0, 365, n), unit="D"),
        "customer_id": rng.integers(1, 301, n),
        "category": rng.choice(
            ["Electronics", "Fashion", "Home", "Books"], n,
            p=[0.30, 0.35, 0.20, 0.15]),
        "amount": rng.gamma(2.0, 600, n).round(2)
    })
    orders.to_csv(DATA_FILE, index=False)

orders = pd.read_csv(DATA_FILE, parse_dates=["order_date"])

# Data quality checks.
print("Shape:", orders.shape)
print("\nData types:\n", orders.dtypes)
print("\nMissing values:\n", orders.isna().sum())
print("Duplicate rows:", orders.duplicated().sum())

# Feature engineering.
orders["month"] = orders["order_date"].dt.to_period("M")
orders["month_start"] = orders["order_date"].dt.to_period("M").dt.to_timestamp()
orders["weekday"] = orders["order_date"].dt.day_name()
orders["quarter"] = orders["order_date"].dt.quarter

# Monthly revenue and month-over-month growth.
monthly = orders.groupby("month_start")["amount"].sum().sort_index()
monthly_growth = monthly.pct_change() * 100
print("\nMonthly revenue and growth:")
print(pd.DataFrame({"revenue": monthly, "growth_pct": monthly_growth}).round(2))
print("Best month:", monthly.idxmax(), "| Lowest month:", monthly.idxmin())

# Category summary and month-by-category pivot table.
by_category = (orders.groupby("category")["amount"]
               .agg(total_revenue="sum", average_order_value="mean", order_count="count")
               .sort_values("total_revenue", ascending=False))
print("\nCategory performance:\n", by_category.round(2))
pivot = pd.pivot_table(orders, index="month_start", columns="category",
                       values="amount", aggfunc="sum", fill_value=0)
print("\nMonthly category pivot:\n", pivot.round(2))

# Customer spend and Pareto-style top 10% revenue share.
spend = orders.groupby("customer_id")["amount"].sum().sort_values(ascending=False)
top_n = max(1, int(np.ceil(len(spend) * 0.10)))
top_share = spend.head(top_n).sum() / spend.sum()
print(f"\nTop 10% ({top_n}) of customers contribute {top_share:.1%} of revenue.")

# Four-panel dashboard.
sns.set_theme(style="whitegrid", palette="deep")
fig, axes = plt.subplots(2, 2, figsize=(13, 9), constrained_layout=True)
fig.suptitle("E-commerce Sales Analysis — 2025 Simulated Orders",
             fontsize=16, fontweight="bold")

axes[0, 0].plot(monthly.index, monthly.values, marker="o", linewidth=2)
axes[0, 0].scatter([monthly.idxmax()], [monthly.max()], s=90, label="Best month")
axes[0, 0].scatter([monthly.idxmin()], [monthly.min()], s=90, label="Lowest month")
axes[0, 0].set(title="Monthly revenue trend", xlabel="Month", ylabel="Revenue (USD)")
axes[0, 0].tick_params(axis="x", rotation=35)
axes[0, 0].legend()

cat = by_category["total_revenue"].sort_values()
axes[0, 1].barh(cat.index, cat.values)
axes[0, 1].set(title="Revenue by category", xlabel="Revenue (USD)", ylabel="Category")

for category in pivot.columns:
    axes[1, 0].plot(pivot.index, pivot[category], marker=".", label=category)
axes[1, 0].set(title="Monthly revenue by category", xlabel="Month", ylabel="Revenue (USD)")
axes[1, 0].tick_params(axis="x", rotation=35)
axes[1, 0].legend(title="Category", fontsize=8)

cumulative_revenue_share = spend.cumsum() / spend.sum() * 100
cumulative_customer_share = np.arange(1, len(spend) + 1) / len(spend) * 100
axes[1, 1].plot(cumulative_customer_share, cumulative_revenue_share)
axes[1, 1].axvline(10, linestyle="--", label="Top 10% of customers")
axes[1, 1].axhline(top_share * 100, linestyle="--", label=f"Revenue share: {top_share:.1%}")
axes[1, 1].set(title="Customer revenue concentration",
               xlabel="Cumulative share of customers (%)",
               ylabel="Cumulative share of revenue (%)", xlim=(0, 100), ylim=(0, 100))
axes[1, 1].legend(fontsize=8)

fig.savefig(DASHBOARD_FILE, dpi=150, bbox_inches="tight")
plt.show()
print(f"Dashboard saved to: {DASHBOARD_FILE}")
