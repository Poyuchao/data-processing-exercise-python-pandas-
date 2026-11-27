import re
import pandas as pd 

# load 
tw_df = pd.read_csv("tw_sessions.csv",encoding="utf-8-sig")
uk_df = pd.read_json("uk_sessions.json")
us_df = pd.read_csv("us_sessions.csv")

# inspect 
# print(tw_df)
# print(uk_df)
# print(us_df)

#normalize
def hms_to_sec(s):                      # "00:12:40" -> 760；格式不對回傳 None
    m = re.fullmatch(r"(\d{2}):([0-5]\d):([0-5]\d)", str(s))
    return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) if m else None

def ms_to_sec(s):                       # "12:40" -> 760
    m = re.fullmatch(r"([0-5]\d):([0-5]\d)", str(s))
    return int(m[1]) * 60 + int(m[2]) if m else None

# rename tw_df column and change the tw_df itself
tw_df=tw_df.rename(columns={"場次":"session","醫師":"doctor","時間":"seconds","主題":"theme_raw","內容":"text"}) 
tw_df["seconds"]=tw_df["seconds"].apply(ms_to_sec)

# rename uk_sessions column and change the uk_sessions itself
uk_df=uk_df.rename(columns={"speaker":"doctor","t":"seconds","theme":"theme_raw"}) 
uk_df["seconds"] = uk_df["seconds"].apply(hms_to_sec)

# rename us_df column and change the us_df itself
us_df=us_df.rename(columns={"session_id":"session","physician":"doctor","topic":"theme_raw","quote":"text"}) 


#add the market column into each country df
tw_df.insert(0,"market","TW")
uk_df.insert(0,"market","UK")
us_df.insert(0,"market","US")


# combine each countries df together 
df=pd.concat([tw_df,uk_df,us_df], ignore_index=True)

# data cleaing 
# step 1 convert doctor id to Dr_U1 , str index 0 & 3 to be upper 
df["doctor"]=df["doctor"].str.strip().str.lower()
s= df["doctor"]
df["doctor"]=s.str[0].str.upper() + s.str[1:3]+s.str[3].str.upper()+s.str[4:] # combine each character together s[0] & s[3]= upper 

# step 2 rows with a missing doctor, or a time that is not valid, go to a "bad rows" list
bad_rows_doctors=df[df["doctor"].isna()] # missing doctor name
# to avoid missing doctor name and also invalid time to be counted twice 
bad_rows_times=df[df["seconds"].isna()& df["doctor"].notna()] # invalid time and doctor has name 
bad_rows_doctors=bad_rows_doctors.assign(reason="missing doctor name") # add reason
bad_rows_times = bad_rows_times.assign(reason="invalid time") # add reason

bad_rows=pd.concat([bad_rows_doctors,bad_rows_times]) # combine bad rows and keep index 
good_rows=df.drop(bad_rows.index) # so drop the bad rows , the rest of them are good rows


# map  the raw themes to 5 themes: hypoglycemia, price_reimbursement, adherence, weight_gain, dosing_convenience
# normalize the raw theme first 
theme_raw= df["theme_raw"].str.strip().str.lower().value_counts(dropna=False)

THEMES={
    "hypoglycemia" : ["hypoglycaemia","低血糖","low blood sugar","hypoglycemia"],
    "price_reimbursement":["reimbursement","健保給付","price","cost","insurance coverage","price_reimbursement"],
    "adherence":["compliance","Adherence","adherence"],
    "weight_gain":["weight gain","weight","體重","體重增加","weight_gain"],
    "dosing_convenience":["once weekly","dosing_convenience","dosing convenience"]
}

SYN={}

for theme, raws in THEMES.items(): # 外層 :逐一取出每個標準主題 和它的清單
    for raw in raws: # 內層: 逐一取出清單裡的每個同義字
        SYN[raw]= theme # 存成同義詞

good_rows["theme"]=good_rows["theme_raw"].str.strip().str.lower().map(SYN)

#remove duplicates on (market, doctor, seconds, theme), keep the last one
good_rows=good_rows.drop_duplicates(subset=["market","doctor","seconds","theme"],keep="last")

#For each theme: how many DISTINCT doctors raised it, and how many mentions?
# group by theme /5 , only see the doctor column , count each group has how many diff doctors
distinct_doctor= good_rows.groupby("theme")["doctor"].nunique()

# how many mentions?
mentions= good_rows["theme"].value_counts()

summary = pd.DataFrame({
    "doctors": distinct_doctor,
    "mentions": mentions,
})
# print(summary)

# For each market: what share of the doctors raised each theme?
n = good_rows.groupby(["market", "theme"])["doctor"].nunique().rename("n").reset_index()

# print(n.pivot(index="theme", columns="market", values="n"))

# # print(df.to_string(index=False))

# print(bad_rows)


print(good_rows)

# load doctor profile data
doc_pf_csv=pd.read_csv("doctors.csv")

# inspect 
# print(doc_pf_csv.shape)
# print(doc_pf_csv.to_string(index=False)) # view first 5 data 
# doc_pf_csv.info()# view index , column, how many Non-Null Count in each columns , data type 
# print(doc_pf_csv.isna().sum())     # each columns null count

# which doctors in the sessions have no profile? which profiles have no sessions?
# retrieve the doctor who has no profile in session
A=good_rows["doctor"]
B=doc_pf_csv["doctor_id"]

A = set(A)
B = set(B)

# the doctor who has no profile in session -> A-B  ans = {'Dr_T5'}
print("doctor no profile in session",A-B)


# the doctor which profiles have no session 
print("doctor profiles have no session ",B-A)

#among the doctors who raised hypoglycemia, how many are there per specialty? 
# find rasied hypoglycemia's doctor

C = set(good_rows.loc[good_rows["theme"] == "hypoglycemia", "doctor"])
C=set(C)

print("raised hypoglycemia doctor", C)

# how many are there per specialty-> find rasied hypoglycemia's doctor and group by speciality 
# using isin([...]) to pick up the data from doctor.csv in c 

hypo_profiles= doc_pf_csv[doc_pf_csv["doctor_id"].isin(C)]

# retrieve how many per specialty in this df 

# print(len(C))
# print(hypo_profiles["specialty"].value_counts().sum())
# print(hypo_profiles["specialty"].value_counts())

# print("doctor no profile but raised hypoglycemia" , C - set(hypo_profiles["doctor_id"]))


hypo = good_rows.loc[good_rows["theme"] == "hypoglycemia", ["doctor","theme"]].drop_duplicates()

print(hypo)

m = hypo.merge(doc_pf_csv[["doctor_id", "specialty"]],
               left_on="doctor", right_on="doctor_id", how="left")

print(m["specialty"].fillna("no profile / blank").value_counts())
