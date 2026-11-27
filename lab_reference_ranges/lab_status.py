import numpy as np
import pandas as pd

lab_csv=pd.read_csv("lab_results.csv")
ref_csv=pd.read_csv("reference_ranges.csv")

print(lab_csv.head())
# print(lab_csv.dtypes)

print(ref_csv.head())
# print(ref_csv.dtypes)

# patient_id: remove spaces, upper case (P001)
lab_csv["patient_id"]=lab_csv["patient_id"].str.strip().str.upper()
# test: remove spaces, lower case (glucose) 
lab_csv["test"]=lab_csv["test"].str.strip().str.lower()
# value: make it a number; things like "N/A" or "high" become missing
lab_csv["value"]=pd.to_numeric(lab_csv["value"],errors="coerce")
# Print how many values could not be converted.
value_not_convert= lab_csv["value"].isna().sum()
print("missing value", value_not_convert)

ref_csv["test"]=ref_csv["test"].str.strip().str.lower()
# merge both table 
merged_tb= lab_csv.merge(ref_csv, left_on="test", right_on="test", how="left")
merged_tb=merged_tb.assign(status="normal")
merged_tb.loc[merged_tb["value"]<merged_tb["low"],"status"]="low"
merged_tb.loc[merged_tb["value"]>merged_tb["high"],"status"]="high"
merged_tb.loc[merged_tb["value"].isna() | merged_tb["low"].isna(), "status"] = "unknown"


#  For each test: number of distinct patients,
# mean value, and the share of rows with status "high" or "low".

merged_tb["is_abnormal"] = merged_tb["status"].isin(["high", "low"])

ans = merged_tb.groupby("test").agg({"patient_id":"nunique","value":"mean", "is_abnormal":"mean"})
# print(merged_tb)
print(ans)


