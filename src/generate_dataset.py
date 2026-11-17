"""Generate a synthetic personal expense dataset for 2025.

The dataset is practice data only. It contains 420 expense transactions
across the year 2025 so the Pandas, NumPy and visualization workflow can be
practised on realistic personal-finance data.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "personal_expenses_2025.csv"

AMOUNT_RANGES = {
    "Food": (150, 1500),
    "Transport": (50, 800),
    "Rent": (12000, 18000),
    "Shopping": (500, 8000),
    "Bills": (800, 4500),
    "Entertainment": (300, 3000),
    "Health": (500, 6000),
    "Education": (1000, 10000),
}

ESSENTIAL = {"Food", "Transport", "Rent", "Bills", "Health", "Education"}


def main() -> None:
    rng = np.random.default_rng(42)
    total_rows = 420

    # Rent: exactly one transaction per month (12 rows).
    rent_rows = []
    for month in range(1, 13):
        day = int(rng.integers(1, 6))
        low, high = AMOUNT_RANGES["Rent"]
        rent_rows.append(
            {
                "date": pd.Timestamp(year=2025, month=month, day=day),
                "category": "Rent",
                "amount_bdt": round(float(rng.uniform(low, high)), 2),
            }
        )

    # The remaining 408 transactions are spread randomly over 2025.
    other_categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Education"]
    probabilities = [0.60, 0.25, 0.015, 0.06, 0.035, 0.01, 0.03]
    n_other = total_rows - len(rent_rows)
    categories = rng.choice(other_categories, size=n_other, p=probabilities)

    start = pd.Timestamp("2025-01-01")
    day_offsets = rng.integers(0, 365, size=n_other)
    dates = start + pd.to_timedelta(day_offsets, unit="D")

    other_rows = []
    for date, category in zip(dates, categories):
        low, high = AMOUNT_RANGES[category]
        other_rows.append(
            {
                "date": date,
                "category": category,
                "amount_bdt": round(float(rng.uniform(low, high)), 2),
            }
        )

    df = pd.DataFrame(rent_rows + other_rows)
    df["month"] = df["date"].dt.month
    df["payment_method"] = rng.choice(
        ["Cash", "bKash", "Nagad", "Card"], size=len(df), p=[0.40, 0.30, 0.12, 0.18]
    )
    df["is_essential"] = df["category"].isin(ESSENTIAL)

    df = df.sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df = df[["date", "month", "category", "amount_bdt", "payment_method", "is_essential"]]

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset created: {DATA_PATH}")
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
