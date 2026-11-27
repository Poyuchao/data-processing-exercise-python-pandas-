import numpy as np
import pandas as pd


uk_csv=pd.read_csv("feedback_uk.csv")
us_json=pd.read_json("feedback_us.json")

# print(uk_csv.head())

# print(uk_csv)

# print(us_json.head())



# convert the positive , neutral, negative to corresponding number
MAP = {1:"negative",2:"negative",3:"neutral",4:"positive",5:"positive"}
us_json["sentiment"]=us_json["sentiment"].map(MAP)


# print(us_json)
uk_csv.insert(0, "market", "UK")
us_json.insert(0, "market", "US")

uk_csv["date"]  = pd.to_datetime(uk_csv["date"],  format="%d/%m/%Y", errors="coerce")
us_json["date"] = pd.to_datetime(us_json["date"], format="%Y-%m-%d", errors="coerce")


all_df= pd.concat([uk_csv,us_json],ignore_index=True).drop(columns=["id"])
all_df["sentiment"]=all_df["sentiment"].str.strip().str.lower()

# cleaning  clinician IDs should look like Dr_K1 
s=all_df["clinician"].str.strip()  # remove space 
all_df["clinician"]=s.str[0].str.upper()+ s.str[1].str.lower()+"_"+s.str[3].str.upper()+s.str[4:]

# topics: lower case, no extra spaces, and "side-effects" should be "side effects"

all_df["topic"]=all_df["topic"].str.lower().str.strip()

all_df.loc[all_df["topic"].str.contains("effect"),"topic"]="side effects"

print(all_df)
# rows with a missing clinician or an invalid date go to a "bad rows" list with a reason
# (count each row once: check the clinician first, then the date) 
bad_row_clinician= all_df[all_df["clinician"].isna()]
bad_row_clinician = bad_row_clinician.assign(reason="missing clinician")
bad_row_date= all_df[all_df["date"].isna()&~all_df["clinician"].isna()]
bad_row_date = bad_row_date.assign(reason="invalid date")
all_bad_row= pd.concat([bad_row_clinician,bad_row_date ])

all_good_row= all_df.drop(all_bad_row.index)  # drop bad row index so remaining are good rows
print(all_bad_row)

# - remove duplicates on (market, clinician, date, topic), keep the last one
all_good_row = all_good_row.drop_duplicates(subset=["market", "clinician", "date", "topic"],keep="last")
print(all_good_row)

#For each topic: how many distinct clinicians raised it, 
distinct_clinicians_raised=all_good_row.groupby("topic")["clinician"].nunique()
# and how many mentions? 
mentions=all_good_row["topic"].value_counts()
print(distinct_clinicians_raised)
print(mentions)


# 3.For each market: what share of the feedback is negative?
neg_count = all_good_row[all_good_row["sentiment"] == "negative"].groupby("market").size()
total     = all_good_row.groupby("market").size()

print(neg_count/total)

