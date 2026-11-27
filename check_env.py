"""Quick sanity check for the Python / pandas environment."""
import sys
import io

import numpy as np
import pandas as pd

print("Python :", sys.version.split()[0])
print("pandas :", pd.__version__)
print("numpy  :", np.__version__)

csv = io.StringIO(
    """order_id,customer,date,amount
1,Alice,2026-01-03,120.5
2,Bob,2026-01-04,
3,Alice,2026-02-10,80
4,Carol,2026-02-11,200
"""
)
df = pd.read_csv(csv, parse_dates=["date"])
df["amount"] = df["amount"].fillna(0)
df["month"] = df["date"].dt.to_period("M")

print("\nRaw data:\n", df)
print("\nTotal by customer:\n", df.groupby("customer")["amount"].sum().sort_values(ascending=False))
print("\nPivot (customer x month):\n", df.pivot_table(index="customer", columns="month", values="amount", aggfunc="sum", fill_value=0))
print("\nEnvironment OK ✅")
