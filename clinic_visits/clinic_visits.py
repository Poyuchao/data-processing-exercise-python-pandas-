"""Clinic visit analysis: totals, averages, date filters, text matching and joins.
Run:  python clinic_visits.py     (prints PASS / FAIL for each result check)
"""
import numpy as np
import pandas as pd

visits = pd.read_csv("visits.csv")
clinics = pd.read_csv("clinics.csv")
print(visits.shape, clinics.shape)
print(visits)
print(clinics)
# ---- Task 1 ----
# Total minutes per clinic. Return a Series sorted from the largest to the smallest.

df1= visits.groupby("clinic")["minutes"]
df1=df1.sum().sort_values(ascending=False)
# print(df1)

r1 =df1

# ---- Task 2 ----
# Average rating per clinic (missing ratings are ignored), rounded to 2 decimals. Return a
# dict like {"North": 4.0, ...}.

df2= visits.groupby("clinic")["rating"].mean().round(2)
# print(df2)

#  Group the visits by clinic and take the mean rating of each clinic. mean() skips missing ratings, so they are not counted.

r2 = df2.to_dict()

# ---- Task 3 ----
# Which visits have no rating? Return a sorted list of visit_id.
df3= visits["visit_id"][visits["rating"].isna()]
# print(sorted(df3))
r3 = sorted(df3)

# retrieve the visit id with no rating 

# ---- Task 4 ----
# Convert the date column to real dates. How many visits happened on or after 2026-10-05?
# Return an int.
d=pd.to_datetime(pd.Series(visits["date"])) # str to date type 
# list the date on or after 2026-10-05 , d
# print(d[d >= "2026-10-05" ])

r4 = int((d >= "2026-10-05").sum())

# ---- Task 5 ----
# How many visits have a note that mentions "price" (any capitalization)? Return an int.
df5=visits["note"].str.lower().str.contains("price")

# using sum to count the true
# print(df5.sum())

# if counting false use ~ -> (~df5).sum() or len(df5) - df5.sum() origin - true counts

r5 = df5.sum()

# ---- Task 6 ----
# The 3 doctors with the most total minutes. Return a list of doctor ids, most minutes
# first.
df6=visits.groupby("doctor")["minutes"].sum().sort_values(ascending=False).head(3)

# head(3), nlargest(3) = sort_values(ascending=False).head(3)

r6 =(list(df6.index))

# ---- Task 7 ----
# Compare the clinics in visits with the clinics table. Return a tuple of two sets:
# (clinics that have visits but are not in the clinics table, clinics in the table that
# have no visits).
df7_visit_clinic=set(visits["clinic"])
df7_clinic=set(clinics["clinic"])

clinics_have_visits_not_in_clinics = df7_visit_clinic-df7_clinic
clinics_have_no_visits= df7_clinic-df7_visit_clinic

# print(clinics_have_visits_not_in_clinics,clinics_have_no_visits)
r7 = tuple([clinics_have_visits_not_in_clinics,clinics_have_no_visits])

# ---- Task 8 ----
# Add a column category: "price" if the note mentions price, "side effects" if it mentions
# side effect, otherwise "follow-up". Return a dict of how many visits per category.
df8= visits.assign(category="follow-up")
note = df8["note"].str.lower() 
df8.loc[note.str.contains("price"),"category"]="price"
df8.loc[note.str.contains("side effect"),"category"]="side effects"

count_category=df8["category"].value_counts()
r8 = count_category.to_dict()

# ---- Task 9 ----
# For each doctor, the date of their latest visit as a string "YYYY-MM-DD". Return a dict.
dates= visits.assign(date=pd.to_datetime(visits["date"])) 
# "I make a copy of visits where the date column is converted to datetime.
#  Then I group by doctor, take the latest date, and format it back to a 'YYYY-MM-DD' string."
# print(dates.dtypes)
ans= dates.groupby("doctor")["date"].max().dt.strftime("%Y-%m-%d")

r9 = ans.to_dict()

# ---- Task 10 ----
# Call a visit long if minutes >= 30. For every clinic in visits, how many long visits?
# Return a dict (clinics with zero long visits must appear with 0).

visit_long=visits.assign(is_long=0)
visit_long.loc[visit_long["minutes"]>=30, "is_long"]=1
ans= visit_long.groupby("clinic")["is_long"].sum()
 
print(ans.to_dict())
r10 =ans.to_dict()

# ====== Checks ======
checks = {
    "1": lambda: list(r1.items()) == [('South', 170), ('North', 165), ('East', 130), ('West', 20)],
    "2": lambda: dict(r2) == {'East': 3.25, 'North': 4.0, 'South': 4.0, 'West': 4.0},
    "3": lambda: r3 == ['V04', 'V08'],
    "4": lambda: int(r4) == 8,
    "5": lambda: int(r5) == 6,
    "6": lambda: r6 == ['Dr_B2', 'Dr_A2', 'Dr_A1'],
    "7": lambda: r7 == ({'West'}, {'Central'}),
    "8": lambda: dict(r8) == {'price': 6, 'side effects': 4, 'follow-up': 4},
    "9": lambda: dict(r9) == {'Dr_A1': '2026-10-08', 'Dr_A2': '2026-10-05', 'Dr_B1': '2026-10-05', 'Dr_B2': '2026-10-07', 'Dr_C1': '2026-10-06', 'Dr_C2': '2026-10-09', 'Dr_D1': '2026-10-08'},
    "10": lambda: dict(r10) == {'East': 2, 'North': 4, 'South': 3, 'West': 0},
}
for pid, fn in checks.items():
    val = globals()["r" + pid]
    if val is None:
        print(f"Task {pid}: TODO"); continue
    try:
        print(f"Task {pid}: " + ("PASS" if fn() else "FAIL"))
    except Exception as e:
        print(f"Task {pid}: FAIL ({type(e).__name__}: {e})")
