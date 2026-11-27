"""Doctor theme analysis: distinct counts, joins, bad rows, de-duplication and shares by market.
Run:  python theme_analysis.py     (prints PASS / FAIL for each result check)
"""
import pandas as pd
good = pd.read_csv("good.csv")
profiles = pd.read_csv("profiles.csv")
rows = pd.read_csv("rows.csv")
print(good.shape, profiles.shape, rows.shape)
print(good)
print(profiles)

# ---- Task 1 ----
# Which doctors raised hypoglycemia? Return a DataFrame with the columns doctor and theme,
# one row per doctor.
r1= good.loc[good["theme"]=="hypoglycemia",["doctor","theme"]].drop_duplicates()

print(r1.to_string(index=False))

# ---- Task 2 ----
# How many DISTINCT doctors raised each theme? Return a Series sorted from most to least.

r2 = good.groupby("theme")["doctor"].nunique().sort_values(ascending=False)


# ---- Task 3 ----
# How many MENTIONS (rows) does each theme have? Return a Series.
r3 = good["theme"].value_counts()


# print(r3)

# ---- Task 4 ----
# For each market and theme, how many distinct doctors? Return a normal DataFrame with the
# columns market, theme, n.
r4 = good.groupby(["market","theme"])["doctor"].nunique().rename("n").reset_index()
print(r4)

# print(r4)

# ---- Task 5 ----
# Which doctors appear in good but have no profile? Return a set.

A=good["doctor"]

A=set(A)

B=profiles["doctor_id"]

B=set(B)

r5 = A-B 

# ---- Task 6 ----
# Attach each doctor's specialty to good (keep ALL rows of good). Doctors without a
# profile, or with a blank specialty, should show "no profile". Return a Series: the
# number of ROWS per specialty.

# all doctor
A=good

# doctor profile
B=profiles[["doctor_id","specialty"]]

merged=A.merge(B,left_on="doctor", right_on="doctor_id", how="left")  # A merge B , left table use doctor , right table use doctor_id, and keep the remaining in left
merged[["specialty"]]=merged[["specialty"]].fillna("no profile")

r6 = merged["specialty"].value_counts()

# print(r6)

# ---- Task 7 ----
# In rows, find the rows where the doctor is present but seconds is missing. Add a column
# reason = "invalid time". Return a DataFrame.


dr_sc=rows
print(dr_sc)
bad_rows_doctor=dr_sc[dr_sc["doctor"].isna()]
bad_rows_time=dr_sc[dr_sc["seconds"].isna()&dr_sc["doctor"].notna()] # to avoid the edge case, the row missing doctor and time values
bad_rows_time=bad_rows_time.assign(reason="invalid time")

# print(bad_rows_time)

r7 =bad_rows_time

# ---- Task 8 ----
# Remove duplicates on (market, doctor, theme), keeping the LAST one. Return a DataFrame
# (all original columns).
df8=good
df8=df8.drop_duplicates(subset=["market","doctor","theme"],keep="last")
r8 = df8

# ---- Task 9 ----
# Which doctors raised MORE THAN ONE different theme? Return a sorted list of doctor ids.


themes_count=good.groupby(["doctor"])["theme"].nunique().sort_values()

multi_theme = themes_count[themes_count > 1]

r9 = sorted(multi_theme.index)
# print(sorted(r9))

# ---- Task 10 ----
# For each market, what share of its doctors raised hypoglycemia? Return a dict like
# {"UK": 0.5, ...} (round to 2 decimals).

doc_mentions_hy=good.loc[good["theme"]=="hypoglycemia",["market","doctor"]]

all_doctors=good.groupby("market")["doctor"].nunique()
hypo_doctors =doc_mentions_hy.groupby("market")["doctor"].nunique()
print(all_doctors)

r10 = (hypo_doctors / all_doctors).round(2).to_dict()


# ====== Checks ======
checks = {
    "1": lambda: set(r1["doctor"]) == {"Dr_U1","Dr_T1","Dr_T2","Dr_A1"} and len(r1) == 4 and list(r1.columns) == ["doctor","theme"],
    "2": lambda: r2.to_dict() == {"hypoglycemia":4,"price_reimbursement":2,"adherence":2,"weight_gain":1} and r2.iloc[0] == 4 and r2.iloc[-1] == 1,
    "3": lambda: r3.to_dict() == {"hypoglycemia":5,"price_reimbursement":2,"adherence":2,"weight_gain":1},
    "4": lambda: list(r4.columns) == ["market","theme","n"] and len(r4) == 8 and int(r4.loc[(r4.market=="US")&(r4.theme=="hypoglycemia"),"n"].iloc[0]) == 1 and int(r4.loc[(r4.market=="TW")&(r4.theme=="hypoglycemia"),"n"].iloc[0]) == 2,
    "5": lambda: r5 == {"Dr_A2","Dr_T5"},
    "6": lambda: r6.to_dict() == {"no profile":4,"endocrinology":2,"cardiology":2,"primary care":1,"internal medicine":1},
    "7": lambda: list(r7.index) == [2,4] and set(r7["reason"]) == {"invalid time"} and "reason" in r7.columns,
    "8": lambda: len(r8) == 9 and list(r8.columns) == ["market","doctor","theme","seconds"] and 6 not in r8.index and 8 in r8.index,
    "9": lambda: list(r9) == ["Dr_A2","Dr_U1"],
    "10": lambda: r10 == {"UK":0.5,"TW":0.67,"US":0.5},
}

for pid, fn in checks.items():
    val = globals()["r" + pid]
    if val is None:
        print(f"Task {pid}: TODO"); continue
    try:
        print(f"Task {pid}: " + ("PASS" if fn() else "FAIL"))
    except Exception as e:
        print(f"Task {pid}: FAIL ({type(e).__name__}: {e})")
