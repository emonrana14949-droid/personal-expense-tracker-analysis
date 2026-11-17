"""Analyse the personal expense dataset with Pandas, NumPy and Matplotlib.

Run from the project root:
    python src/analysis.py

Outputs are saved to:
    outputs/tables/  (CSV summary tables)
    outputs/charts/  (PNG visualizations)
    outputs/insights.md
"""

import calendar
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "personal_expenses_2025.csv"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"
INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "insights.md"

try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")


def monthly_income() -> pd.DataFrame:
    """Fixed salary of 55,000 BDT/month plus small seeded variation."""
    rng = np.random.default_rng(7)
    variation = rng.integers(-1500, 2501, size=12)
    return pd.DataFrame(
        {"month": range(1, 13), "income_bdt": 55000 + variation}
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.drop_duplicates().copy()
    df["amount_bdt"] = pd.to_numeric(df["amount_bdt"], errors="coerce")
    df = df.dropna(subset=["amount_bdt"])
    df["month"] = df["date"].dt.month

    # Summary statistics.
    df.describe(include="all").round(2).to_csv(TABLE_DIR / "summary_statistics.csv")

    # Monthly summary with income, savings and savings rate.
    monthly = (
        df.groupby("month")
        .agg(total_expenses=("amount_bdt", "sum"), transaction_count=("amount_bdt", "count"))
        .reindex(range(1, 13), fill_value=0)
        .reset_index()
    )
    monthly = monthly.merge(monthly_income(), on="month", how="left")
    monthly["savings_bdt"] = (monthly["income_bdt"] - monthly["total_expenses"]).round(2)
    monthly["total_expenses"] = monthly["total_expenses"].round(2)
    monthly["savings_rate_pct"] = (monthly["savings_bdt"] / monthly["income_bdt"] * 100).round(2)
    monthly.to_csv(TABLE_DIR / "monthly_spending_summary.csv", index=False)

    # Spending by category.
    total_spent = df["amount_bdt"].sum()
    by_category = (
        df.groupby("category")
        .agg(
            total_amount=("amount_bdt", "sum"),
            average_amount=("amount_bdt", "mean"),
            transaction_count=("amount_bdt", "count"),
        )
        .round(2)
    )
    by_category["share_pct"] = (by_category["total_amount"] / total_spent * 100).round(2)
    by_category = by_category.sort_values("total_amount", ascending=False)
    by_category.to_csv(TABLE_DIR / "spending_by_category.csv")

    # Spending by payment method.
    by_payment = (
        df.groupby("payment_method")
        .agg(
            total_amount=("amount_bdt", "sum"),
            average_amount=("amount_bdt", "mean"),
            transaction_count=("amount_bdt", "count"),
        )
        .round(2)
    )
    by_payment["share_pct"] = (by_payment["total_amount"] / total_spent * 100).round(2)
    by_payment = by_payment.sort_values("total_amount", ascending=False)
    by_payment.to_csv(TABLE_DIR / "spending_by_payment_method.csv")

    # Chart 1: monthly spending trend — expenses vs income.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["month"], monthly["total_expenses"], marker="o", color="#2f81f7", label="Expenses")
    ax.plot(monthly["month"], monthly["income_bdt"], marker="s", color="#1a7f37", label="Income")
    ax.set_xticks(range(1, 13), [calendar.month_abbr[m] for m in range(1, 13)])
    ax.set_title("Monthly Spending Trend 2025 — Expenses vs Income", fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (BDT)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "monthly_spending_trend.png", dpi=160)
    plt.close(fig)

    # Chart 2: total spending by category.
    fig, ax = plt.subplots(figsize=(9, 4.8))
    by_category["total_amount"].plot(kind="bar", ax=ax, color="#8250df", edgecolor="white")
    ax.set_title("Total Spending by Category", fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total amount (BDT)")
    ax.tick_params(axis="x", rotation=25)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "spending_by_category.png", dpi=160)
    plt.close(fig)

    # Chart 3: essential vs non-essential spending.
    essential_totals = df.groupby("is_essential")["amount_bdt"].sum()
    essential_totals.index = ["Non-essential" if not idx else "Essential" for idx in essential_totals.index]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    essential_totals.plot(kind="bar", ax=ax, color=["#f778ba", "#2f81f7"][: len(essential_totals)], edgecolor="white")
    ax.set_title("Essential vs Non-Essential Spending", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Total amount (BDT)")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "essential_vs_non_essential.png", dpi=160)
    plt.close(fig)

    # Chart 4: distribution of transaction amounts with mean line.
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.hist(df["amount_bdt"], bins=25, color="#2f81f7", edgecolor="white")
    ax.axvline(df["amount_bdt"].mean(), color="#111111", linestyle="--", linewidth=1.5, label="Mean")
    ax.set_title("Distribution of Transaction Amounts", fontweight="bold")
    ax.set_xlabel("Amount (BDT)")
    ax.set_ylabel("Number of transactions")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "daily_spending_distribution.png", dpi=160)
    plt.close(fig)

    # Key findings.
    top_month_row = monthly.loc[monthly["total_expenses"].idxmax()]
    top_month_name = calendar.month_name[int(top_month_row["month"])]
    top_category = by_category.index[0]
    top_category_share = by_category.loc[top_category, "share_pct"]
    avg_savings_rate = monthly["savings_rate_pct"].mean()
    essential_share = essential_totals.get("Essential", 0) / total_spent * 100

    insights = f"""# Key Insights — Personal Expense Tracker Analysis

> This project uses synthetic practice data generated with NumPy. The patterns below are for learning the workflow only; they are not real financial records.

- Dataset size: **{len(df)} transactions** across 2025, total spending **{total_spent:,.2f} BDT**.
- The highest spending month was **{top_month_name}** with **{top_month_row['total_expenses']:,.2f} BDT** in expenses.
- The top spending category is **{top_category}**, taking **{top_category_share:.2f}%** of all spending.
- Average monthly savings rate: **{avg_savings_rate:.2f}%** of income (income modelled as 55,000 BDT/month plus small variation).
- Essential spending (Food, Transport, Rent, Bills, Health, Education) makes up **{essential_share:.2f}%** of total spending.

## Charts

- `charts/monthly_spending_trend.png`
- `charts/spending_by_category.png`
- `charts/essential_vs_non_essential.png`
- `charts/daily_spending_distribution.png`

## Important note

This is synthetic practice data. For real use, replace the CSV with your own exported transactions and keep personal financial data private.
"""
    INSIGHTS_PATH.write_text(insights, encoding="utf-8")

    print("Analysis complete.")
    print(f"Tables saved to: {TABLE_DIR}")
    print(f"Charts saved to: {CHART_DIR}")
    print(f"Insights saved to: {INSIGHTS_PATH}")
    print(f"Highest spending month: {top_month_name} ({top_month_row['total_expenses']:,.2f} BDT)")
    print(f"Top category: {top_category} ({top_category_share:.2f}%)")
    print(f"Average monthly savings rate: {avg_savings_rate:.2f}%")


if __name__ == "__main__":
    main()
