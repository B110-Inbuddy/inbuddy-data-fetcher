import os
import pandas as pd

TEST = False
PATH = "/Users/seojeong/Downloads/data"

path = PATH + ("_test" if TEST else "")

df = pd.read_csv(path + "/항공기출발현황_20070101-20240307.csv", encoding="cp949")
# col_range = df["현황 : 사유"]
reasons = set(df["사유"].dropna())
statuses = set(df["현황"].dropna())

# print("==reason==")
# for reason in reasons:
#     print(reason)
#
# print("==status==")
# for status in statuses:
#     print(status)


for idx, row in df.iterrows():
    if row['현황'] == "도착":
        print(row)

print(df.head(1))
