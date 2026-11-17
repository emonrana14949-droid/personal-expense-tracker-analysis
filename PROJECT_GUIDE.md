# Project Guide — Personal Expense Tracker Analysis

This guide explains the whole project in simple words, step by step. If you are new to Data Science, start here. After reading this guide, you should be able to run the project, understand every file, and explain the code to anyone.

---

## 1. What is this project?

This project studies **personal money spending for one year (2025)**.

We have a list of **420 expense transactions**. Each transaction is one time money was spent — for example, 331.40 BDT for Food on 2 January 2025, paid by Card.

The project uses Python to answer five questions:

1. Which month has the highest spending?
2. Which category takes the biggest share of total spending?
3. How much is saved each month, and what is the average savings rate?
4. Do essential expenses dominate, or non-essential ones?
5. Which payment method is used for the largest spending?

**Very important:** the dataset is **synthetic practice data**. That means a Python program *created* the data. It is not a real person's money record. The numbers look realistic, so we can practise the full workflow safely: generate data → clean it → analyse it → draw charts → write insights. Later, the same code can be used with real data.

The three tools used are:

| Tool | Job in this project |
|---|---|
| **NumPy** | Creates the fake (synthetic) data and does number work |
| **Pandas** | Loads, cleans and summarises the data in tables |
| **Matplotlib** | Draws the charts |

---

## 2. What is inside the project?

Here is every folder and file, one by one.

```text
personal-expense-tracker-analysis/
├── README.md
├── PROJECT_GUIDE.md
├── requirements.txt
├── .gitignore
├── data/
│   └── personal_expenses_2025.csv
├── src/
│   ├── generate_dataset.py
│   └── analysis.py
├── notebooks/
│   └── personal_expense_analysis.ipynb
└── outputs/
    ├── insights.md
    ├── tables/
    │   ├── summary_statistics.csv
    │   ├── monthly_spending_summary.csv
    │   ├── spending_by_category.csv
    │   └── spending_by_payment_method.csv
    └── charts/
        ├── monthly_spending_trend.png
        ├── spending_by_category.png
        ├── essential_vs_non_essential.png
        └── daily_spending_distribution.png
```

- **README.md** — the short front page of the project. It gives the summary, the questions, and the quick-start commands.
- **PROJECT_GUIDE.md** — this file. The full, slow, beginner-friendly explanation of everything.
- **requirements.txt** — the list of Python libraries the project needs: `pandas`, `numpy` and `matplotlib`, one per line. `pip` reads this file and installs them all at once.
- **.gitignore** — tells Git which files *not* to upload, like `__pycache__/` (automatic Python cache files) and `.venv/`. It keeps the repository clean.
- **data/personal_expenses_2025.csv** — the dataset. One row per transaction, 420 rows, 6 columns. It is created by `src/generate_dataset.py`.
- **src/generate_dataset.py** — the first script. It *creates* the dataset with NumPy and saves it as the CSV file.
- **src/analysis.py** — the second script. It reads the CSV, cleans it, makes all summary tables and charts, and writes the insights file.
- **notebooks/personal_expense_analysis.ipynb** — a Jupyter notebook version for exploring the data step by step interactively: load the data, see the first rows, make a category table, draw one chart.
- **outputs/tables/** — CSV files with the summary numbers (explained in Section 7).
- **outputs/charts/** — PNG image files with the four charts (explained in Section 7).
- **outputs/insights.md** — the final written findings of the project: the key numbers in plain sentences.

The `outputs/` files are **not** typed by hand. They are created automatically every time you run `src/analysis.py`.

---

## 3. The dataset, column by column

The file `data/personal_expenses_2025.csv` has **420 rows** and **6 columns**. The first rows look like this:

```text
date,month,category,amount_bdt,payment_method,is_essential
2025-01-01,1,Rent,14633.27,bKash,True
2025-01-02,1,Transport,307.04,Cash,True
2025-01-02,1,Food,331.40,Card,True
```

Now each column:

### `date`
The day the money was spent, written as year-month-day. Example: `2025-01-02` means 2 January 2025. All dates are inside the year 2025.

### `month`
The month number taken from the date: `1` = January, `2` = February, up to `12` = December. This column makes it easy to group spending month by month.

### `category`
What the money was spent on. There are 8 categories:

| Category | Example spending | Typical amount in this data |
|---|---|---|
| Food | meals, groceries | 150–1,500 BDT |
| Transport | bus, rickshaw, fuel | 50–800 BDT |
| Rent | house rent, once a month | 12,000–18,000 BDT |
| Shopping | clothes, gadgets | 500–8,000 BDT |
| Bills | electricity, internet, phone | 800–4,500 BDT |
| Entertainment | movies, games, eating out for fun | 300–3,000 BDT |
| Health | medicine, doctor | 500–6,000 BDT |
| Education | books, courses, fees | 1,000–10,000 BDT |

Food is the most common category (247 of the 420 transactions). Rent is rare — only 12 transactions, one per month — but each one is big.

### `amount_bdt`
How much money was spent in that transaction, in Bangladeshi Taka (BDT). Example: `14633.27` means 14,633.27 taka (that row is a Rent payment). Most transactions are small; a few, like Rent, are very large.

### `payment_method`
How the money was paid. Four options: `Cash`, `bKash`, `Nagad` and `Card`. In the generator, Cash is picked most often (40% chance), then bKash (30%), Card (18%) and Nagad (12%).

### `is_essential`

`True` or `False`. It tells whether the category is a basic need.

- **Essential (True):** Food, Transport, Rent, Bills, Health, Education — things a person must pay for.
- **Non-essential (False):** Shopping and Entertainment — things that are nice, but can be reduced.

This one column lets the analysis compare "needs" against "wants". In this project, 91.99% of all spending is essential.

### Where are income and savings? (Not in this file!)

The CSV has only spending. There is **no income column**. Income is created inside `src/analysis.py`, in a small function called `monthly_income()`:

- Salary is modelled as **55,000 BDT per month**.
- A small random change is added: between −1,500 and +2,500 BDT (with its own seed, 7, so it is the same every run). Example: January's income is 57,280 BDT.
- **Savings** for a month = income − that month's total expenses.
- **Savings rate** = savings ÷ income × 100. It tells what percentage of the income was kept.

Keeping income separate is a design choice: the dataset records spending only, and the analysis joins income next to the monthly spending table.

---

## 4. How to run the project from zero

Follow these steps in order. You need a computer with a terminal (Command Prompt, PowerShell, or any Linux/macOS terminal).

**Step 1 — Install Python.** Download Python from [python.org](https://www.python.org/downloads/) and install it. On Windows, tick the box "Add Python to PATH" during install. Check it works:

```bash
python --version
```

You should see something like `Python 3.11.x`. (On some computers, use `python3` instead of `python` in all commands below.)

**Step 2 — Open the project folder in the terminal.**

```bash
cd personal-expense-tracker-analysis
```

**Step 3 — Install the three libraries.**

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs Pandas, NumPy and Matplotlib.

**Step 4 — Generate the dataset.**

```bash
python src/generate_dataset.py
```

You should see a message like "Dataset created: ... Rows: 420 | Columns: 6". This creates `data/personal_expenses_2025.csv`. (The project already contains this file, but you can re-create it any time — with seed 42 you always get the same data.)

**Step 5 — Run the analysis.**

```bash
python src/analysis.py
```

You should see "Analysis complete." plus the top findings printed.

**Step 6 — Look at the outputs.**

- Read the findings: open `outputs/insights.md`
- See the pictures: open the PNG files in `outputs/charts/`
- See the numbers: open the CSV files in `outputs/tables/` (Excel or any text editor can open them)
- Or explore interactively: open `notebooks/personal_expense_analysis.ipynb` in Jupyter or VS Code and run the cells one by one.

That is all. Two commands — generate, then analyse — run the whole project.

---

## 5. Code explanation: `src/generate_dataset.py`

This script **creates** the dataset. It does not analyse anything. We walk through it in the same order as the code.

### Step 1 — Imports and the job of the file

```python
from pathlib import Path

import numpy as np
import pandas as pd
```

The top of the file has a short description (a docstring) saying the data is practice data only. Then it imports `Path` (for file addresses), NumPy (as `np`, for random numbers) and Pandas (as `pd`, for the table). Short names `np` and `pd` are the standard style in Data Science code.

### Step 2 — Saving the paths

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "personal_expenses_2025.csv"
```

The script finds the project folder from its own location. So the code works on any computer, wherever the project is saved. `DATA_PATH` is the full address of the CSV file it will create.

### Step 3 — The amount ranges table

```python
AMOUNT_RANGES = {
    "Food": (150, 1500),
    "Transport": (50, 800),
    "Rent": (12000, 18000),
    ...
}
```

This is a Python **dictionary**. Each category gets a `(low, high)` pair. Later, each transaction amount is picked randomly inside its category's range. This is why Rent is always big and Transport is always small — it makes the fake data realistic.

### Step 4 — The essential list

```python
ESSENTIAL = {"Food", "Transport", "Rent", "Bills", "Health", "Education"}
```

This is a **set** with the 6 essential categories. Shopping and Entertainment are *not* in the set, so they will become the non-essential ones. This set is used at the end to fill the `is_essential` column.

### Step 5 — Starting the generator

```python
def main() -> None:
    rng = np.random.default_rng(42)
    total_rows = 420
```

Everything happens inside a `main()` function. `rng` is the random number generator, created with **seed 42**.

**Why a seed?** A seed fixes the starting point of the randomness. With seed 42, the "random" numbers come out in the same order every run. So you, your teacher, and anyone else all get the *exact same dataset* and the same results. Without a seed, every run would give different data.

### Step 6 — Rent rows: exactly one per month

```python
rent_rows = []
for month in range(1, 13):
    day = int(rng.integers(1, 6))
    low, high = AMOUNT_RANGES["Rent"]
    rent_rows.append({... "category": "Rent", "amount_bdt": ...})
```

Rent is special: in real life it is paid once a month. So the code loops over months 1 to 12 and makes **exactly 12 rent rows**. The payment day is random from day 1 to day 5 of the month. The amount is a random number between 12,000 and 18,000 BDT, made by `rng.uniform(low, high)` and rounded to 2 decimals.

### Step 7 — The other 408 transactions

```python
other_categories = ["Food", "Transport", "Shopping", "Bills",
                    "Entertainment", "Health", "Education"]
probabilities = [0.60, 0.25, 0.015, 0.06, 0.035, 0.01, 0.03]
categories = rng.choice(other_categories, size=n_other, p=probabilities)
```

`total_rows` is 420, and 12 rows are Rent, so `n_other` is 408. `rng.choice` picks a category for each of the 408 rows. The `p=` list gives the **probability** of each category. Food has 0.60, so about 60% of these rows are Food — that is why Food ends up with 247 transactions. Health has only 0.01, so it is rare. The probabilities add up to 1.0.

### Step 8 — Random dates in 2025

```python
start = pd.Timestamp("2025-01-01")
day_offsets = rng.integers(0, 365, size=n_other)
dates = start + pd.to_timedelta(day_offsets, unit="D")
```

For each row, the code picks a random number of days from 0 to 364 and adds it to 1 January 2025. So every date falls somewhere inside 2025.

### Step 9 — One amount per transaction

```python
for date, category in zip(dates, categories):
    low, high = AMOUNT_RANGES[category]
    other_rows.append({... "amount_bdt": round(float(rng.uniform(low, high)), 2)})
```

`zip` walks through the dates and categories together, pair by pair. For each pair, the code looks up that category's range and draws one random amount inside it.

### Step 10 — Building the table and adding the last columns

```python
df = pd.DataFrame(rent_rows + other_rows)
df["month"] = df["date"].dt.month
df["payment_method"] = rng.choice(
    ["Cash", "bKash", "Nagad", "Card"], size=len(df), p=[0.40, 0.30, 0.12, 0.18])
df["is_essential"] = df["category"].isin(ESSENTIAL)
```

- The rent rows and other rows are joined into one Pandas **DataFrame** (a table) called `df`.
- `month` is taken from the date: `.dt.month` gives 1–12.
- `payment_method` is chosen randomly for every row: Cash 40%, bKash 30%, Nagad 12%, Card 18%.
- `is_essential`: `.isin(ESSENTIAL)` checks each category against the set. It gives `True` or `False` — exactly the column explained in Section 3.

### Step 11 — Sorting, formatting, and saving

```python
df = df.sort_values("date").reset_index(drop=True)
df["date"] = df["date"].dt.strftime("%Y-%m-%d")
df = df[["date", "month", "category", "amount_bdt", "payment_method", "is_essential"]]
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(DATA_PATH, index=False)
```

The rows are sorted by date, oldest first. Dates are formatted as text like `2025-01-02`. The columns are put in a clean order. `mkdir` makes sure the `data/` folder exists, and `to_csv` saves the table as the CSV file. Finally the script prints how many rows and columns were created.

The last lines of the file:

```python
if __name__ == "__main__":
    main()
```

This means: when you run this file directly, start the `main()` function.

---

## 6. Code explanation: `src/analysis.py`

This is the main script. It turns the raw CSV into tables, charts and insights.

### Step 1 — Imports and paths

The script imports `calendar` (for month names like "April"), `matplotlib.pyplot` (charts), `numpy`, and `pandas`. It sets the paths for the data file, the tables folder, the charts folder, and the insights file.

It also chooses a chart style:

```python
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")
```

It tries a clean grid style first. If that style is not available on the computer, it uses `ggplot` instead. This way the script does not crash on different computers.

### Step 2 — The monthly income function

```python
def monthly_income() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    variation = rng.integers(-1500, 2501, size=12)
    return pd.DataFrame({"month": range(1, 13), "income_bdt": 55000 + variation})
```

This small function builds the income table (see Section 3). It uses its **own seed, 7**, so the income numbers are also the same every run. It returns a table with 12 rows: month and income.

### Step 3 — Loading and cleaning the data

```python
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df.drop_duplicates().copy()
df["amount_bdt"] = pd.to_numeric(df["amount_bdt"], errors="coerce")
df = df.dropna(subset=["amount_bdt"])
df["month"] = df["date"].dt.month
```

Line by line:

- `read_csv` loads the CSV into a DataFrame. `parse_dates=["date"]` tells Pandas the date column is real dates, not plain text.
- `drop_duplicates()` removes any repeated rows.
- `to_numeric(..., errors="coerce")` forces amounts to be numbers. Anything that is not a number becomes `NaN` (missing) instead of crashing.
- `dropna(subset=["amount_bdt"])` removes rows where the amount is missing.
- The `month` column is rebuilt from the date, to be safe.

Good analysis always cleans first. Garbage in, garbage out.

### Step 4 — Table 1: summary statistics

```python
df.describe(include="all").round(2).to_csv(TABLE_DIR / "summary_statistics.csv")
```

`describe()` gives a quick summary of every column: count, mean, minimum, maximum and more for numbers; count, unique values and the most common value for text columns. It is saved as `summary_statistics.csv`.

### Step 5 — Table 2: monthly summary, savings and savings rate

```python
monthly = (
    df.groupby("month")
    .agg(total_expenses=("amount_bdt", "sum"),
         transaction_count=("amount_bdt", "count"))
    .reindex(range(1, 13), fill_value=0)
    .reset_index()
)
monthly = monthly.merge(monthly_income(), on="month", how="left")
monthly["savings_bdt"] = (monthly["income_bdt"] - monthly["total_expenses"]).round(2)
monthly["savings_rate_pct"] = (monthly["savings_bdt"] / monthly["income_bdt"] * 100).round(2)
```

This is the heart of the project:

- `groupby("month")` groups all transactions by month.
- `.agg(...)` adds up each month's spending (`sum`) and counts its transactions (`count`).
- `.reindex(range(1, 13), fill_value=0)` makes sure all 12 months appear, even a month with no transactions (it would get 0).
- `merge` joins the income table next to it, matching on `month`.
- **Savings** = income − expenses.
- **Savings rate** = savings ÷ income × 100, as a percentage.

The result is saved as `monthly_spending_summary.csv`. Example: in January, expenses were 42,479.34 BDT, income was 57,280 BDT, so savings were 14,800.66 BDT and the savings rate was 25.84%.

### Step 6 — Table 3: spending by category

```python
by_category = (
    df.groupby("category")
    .agg(total_amount=("amount_bdt", "sum"),
         average_amount=("amount_bdt", "mean"),
         transaction_count=("amount_bdt", "count"))
    .round(2)
)
by_category["share_pct"] = (by_category["total_amount"] / total_spent * 100).round(2)
by_category = by_category.sort_values("total_amount", ascending=False)
```

Transactions are grouped by category. For each category we get the total, the average transaction, and how many transactions there were. `share_pct` is the category's **share of all spending**: its total ÷ total spending of the whole year × 100. The table is sorted biggest first, so Food (34.14%) is on top. Saved as `spending_by_category.csv`.

### Step 7 — Table 4: spending by payment method

The same `groupby` pattern is used once more, this time on `payment_method`. It shows the total, average, count and share for Cash, bKash, Nagad and Card. Saved as `spending_by_payment_method.csv`.

### Step 8 — Chart 1: monthly spending trend

```python
ax.plot(monthly["month"], monthly["total_expenses"], marker="o", color="#2f81f7", label="Expenses")
ax.plot(monthly["month"], monthly["income_bdt"], marker="s", color="#1a7f37", label="Income")
```

Two lines on one chart: expenses (blue) and income (green), month by month. Month numbers on the x-axis are replaced with short names (Jan, Feb, …) using `calendar.month_abbr`. Saved as `monthly_spending_trend.png`.

### Step 9 — Chart 2: spending by category

```python
by_category["total_amount"].plot(kind="bar", ax=ax, color="#8250df", edgecolor="white")
```

The category table from Step 6 is drawn directly as a purple bar chart. Saved as `spending_by_category.png`.

### Step 10 — Chart 3: essential vs non-essential

```python
essential_totals = df.groupby("is_essential")["amount_bdt"].sum()
essential_totals.index = ["Non-essential" if not idx else "Essential" for idx in essential_totals.index]
```

Spending is grouped by the `is_essential` column (True/False) and added up — just two bars. The True/False labels are renamed to "Essential" and "Non-essential" so the chart is easy to read. Saved as `essential_vs_non_essential.png`.

### Step 11 — Chart 4: distribution of transaction amounts

```python
ax.hist(df["amount_bdt"], bins=25, color="#2f81f7", edgecolor="white")
ax.axvline(df["amount_bdt"].mean(), color="#111111", linestyle="--", linewidth=1.5, label="Mean")
```

A **histogram**: all 420 amounts are put into 25 ranges (bins), and each bar shows how many transactions fall in that range. The dashed black line marks the **mean** (average) transaction amount. Saved as `daily_spending_distribution.png`.

### Step 12 — Writing the insights

At the end, the script finds the key answers from the tables it made:

- the month with the highest expenses: `monthly["total_expenses"].idxmax()`
- the top category: the first row of the sorted category table
- the average savings rate: the mean of the monthly savings rates
- the essential share: essential total ÷ total spending × 100

Then it writes these numbers into a ready-made text template (an f-string) and saves it as `outputs/insights.md`. So the insights file is written **by the code**, from the real numbers — if the data changes, the insights change too. Finally, the script prints a short completion message.

---

## 7. How to read the outputs

### The charts

**`monthly_spending_trend.png`** — two lines: income and expenses. Look at the gap between the lines. A big gap means a good saving month. If the blue line ever goes *above* the green line, that month spent more than it earned. In this data, April's blue line comes closest to the income line.

**`spending_by_category.png`** — one bar per category, biggest first. Look at which bars tower over the others. Here Food and Rent are far bigger than the rest. That tells you where the money really goes.

**`essential_vs_non_essential.png`** — only two bars. Compare their heights. Here the Essential bar is much taller: most money goes to needs, not wants. If the Non-essential bar were close to the Essential bar, that would be a warning sign for a budget.

**`daily_spending_distribution.png`** — the histogram of all amounts. Look at the shape. Most transactions pile up on the left (small amounts, under ~1,500 BDT), with a long thin tail to the right (rare big payments like Rent). The dashed mean line sits to the right of the tallest bars, because the few very large payments pull the average up.

### The tables

**`monthly_spending_summary.csv`** — one row per month: total expenses, transaction count, income, savings, savings rate. Read it to find the best and worst saving months, and to check whether savings stay positive all year.

**`spending_by_category.csv`** — one row per category: total, average, count, share %. Read the `share_pct` column to see each category's slice of the year. Compare `average_amount` with `transaction_count`: Rent has a huge average but only 12 transactions; Food has a small average but 247 transactions — both end up on top.

**`spending_by_payment_method.csv`** — the same summary per payment method. Read it to see whether cash or mobile money (bKash/Nagad) carries most of the spending.

**`summary_statistics.csv`** — the automatic `describe()` summary. Use it as a health check of the dataset: how many rows, the average amount, the smallest and largest amounts, and the most common category and payment method.

---

## 8. Key results of this project

These are the actual results from `outputs/insights.md` (synthetic practice data):

- Dataset size: **420 transactions** across 2025, total spending **579,051.71 BDT**.
- The highest spending month was **April**, with **59,075.07 BDT** in expenses.
- The top spending category is **Food**, taking **34.14%** of all spending (197,683.82 BDT over 247 transactions).
- The second biggest category is **Rent** at **31.57%** (182,781.57 BDT over only 12 transactions).
- Average monthly savings rate: **13.51%** of income (income modelled as 55,000 BDT/month plus small variation).
- Essential spending (Food, Transport, Rent, Bills, Health, Education) makes up **91.99%** of total spending. So only about 8% went to non-essential Shopping and Entertainment.

In short: in this dataset, money goes mostly to food and rent, spending peaks in April, and about 13.5% of income is saved in an average month.

---

## 9. Viva / presentation help

Questions a teacher may ask, with short model answers.

**Q1. What is this project about?**
It analyses one year of personal expenses with Python. It finds where the money goes each month, which categories cost the most, and how much is saved against a monthly income.

**Q2. Which libraries did you use, and for what?**
NumPy created the synthetic dataset and does number work. Pandas loaded, cleaned and summarised the data. Matplotlib drew the charts.

**Q3. Is this real data?**
No, it is synthetic data generated by `generate_dataset.py` with NumPy. It is realistic practice data. The same analysis code works on real data if the CSV is replaced.

**Q4. Why did you use seed 42?**
A seed makes the random data the same every run. Anyone running the code gets the identical dataset and results, so the project is reproducible.

**Q5. What is `groupby`?**
`groupby` is a Pandas tool that splits rows into groups — for example, all transactions of one month, or of one category — so we can calculate a sum, mean or count for each group in one line.

**Q6. How is the savings rate calculated?**
First, savings = income − expenses, for each month. Then savings rate = savings ÷ income × 100. It shows what percentage of the income was kept, not spent.

**Q7. Why separate essential and non-essential spending?**
Because it shows whether money goes to needs or wants. Needs like food and rent are hard to cut. Wants like entertainment are the first place to save from. In this project, 91.99% of spending is essential.

**Q8. Why is income not a column in the dataset?**
The dataset records only spending. Income is a fixed monthly salary, so it is modelled inside `analysis.py` instead: 55,000 BDT per month plus a small variation. Keeping it separate also shows how to join two tables with `merge`.

**Q9. What does the histogram show?**
It shows how transaction amounts are spread out. Most transactions are small, and a few are very large, like rent. The dashed line is the mean amount. The mean is pulled to the right by the few large payments.

**Q10. What are the limitations of this project?**
The data is synthetic, so the findings are for practice, not real life. The income model is also simple — a fixed salary. Real expenses have festivals, emergencies and irregular income, which this simple model does not include.

---

## 10. What to learn next / how to extend

1. **Use your own real data.** Track your real expenses for one month in a spreadsheet, save it in the same CSV format, and run the same analysis on it. Compare your real top category with this project's.

2. **Add a budget check.** Set a monthly budget limit for each category (for example, Food ≤ 18,000 BDT) and make the code print a warning for every category that crosses its limit.

3. **Try more charts.** Add a pie chart of category shares, or a month-by-month stacked bar chart of categories, using the same tables the code already makes.

4. **Learn a little Machine Learning.** Use the monthly table to predict next month's spending with a simple model from `scikit-learn`, and check how close the prediction is.

---

*End of guide. Run the project, look at every chart and table,
and try explaining one chart out loud — that is the best viva practice.*
