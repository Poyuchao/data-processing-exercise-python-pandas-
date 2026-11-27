import pandas as pd

eve_csv=pd.read_csv("events.csv")

# print(eve_csv.head())
# print(eve_csv.dtypes)
# print(eve_csv)

drug_csv=pd.read_csv("drugs.csv")

print(drug_csv.head())
print(drug_csv.dtypes)
print(drug_csv)

#drug: remove spaces, lower case
eve_csv["drug"]=eve_csv["drug"].str.strip().str.lower()
#severity: remove spaces, lower case
eve_csv["severity"]=eve_csv["severity"].str.strip().str.lower()
#onset_date and report_date: make them real dates; invalid ones become missing
eve_csv["onset_date"]= pd.to_datetime(eve_csv["onset_date"],errors="coerce")
eve_csv["report_date"]= pd.to_datetime(eve_csv["report_date"],errors="coerce")
# print(eve_csv.dtypes)
#  event_id can appear twice: keep the LAST row for each event_id
eve_csv=eve_csv.drop_duplicates(subset=["event_id"],keep="last")



print(eve_csv)
#Print how many rows you have after cleaning.
print("rows after cleaning",len(eve_csv))


# add a column dats_to_report
# add a column late
eve_csv=eve_csv.assign(days_to_report=0)

# TODO: convert timedelta to days
eve_csv["days_to_report"]=(eve_csv["report_date"]-eve_csv["onset_date"]).dt.days
eve_csv=eve_csv.assign(late=False)
# is True when days_to_report is more than 7
eve_csv.loc[eve_csv["days_to_report"]>7,"late"]=True
print(eve_csv)


#For each drug: number of events, share of events with severity "severe",
# and mean days_to_report. 
# Add the drug class from drugs.csv and sort by number of events (most first).
merged_tb= eve_csv.merge(drug_csv,left_on="drug", right_on="drug", how="left")
merged_tb["is_severity"]= merged_tb["severity"]=="severe"
# print(merged_tb)



ans=merged_tb.groupby("drug").agg({"event_id":"size","is_severity":"mean","days_to_report":"mean"})
ans = ans.merge(drug_csv, left_on="drug" , right_on="drug",how="left")



# print(merged_tb)
print(ans.sort_values("event_id",ascending=False))