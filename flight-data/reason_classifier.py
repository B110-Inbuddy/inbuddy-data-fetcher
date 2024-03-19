import os
import pandas as pd

TEST = False
PATH = "C:/Users/SSAFY/flights-data/data"

path = PATH + ("_test" if TEST else "")

df = pd.read_csv(path + "/data/항공기출발현황_20070101-20240310.csv", encoding="cp949")
filtered = df[["구분", "현황", "사유"]].drop_duplicates(["현황", "사유"])
filtered = filtered.dropna(subset=["사유"])
results = filtered.loc[filtered.구분 != "화물"]

results.sort_values(by=["구분", "현황", "사유"], inplace=True)

COLUMNS = ["구분", "현황", "사유"]
cat = pd.DataFrame(columns=COLUMNS)

print(results.info())
for row in results.itertuples():
    print(row.구분, row.현황, row.사유)

cat = pd.concat([cat, results], ignore_index=True)

# create csv
filename = f"{PATH}/data/항공기출발현황_사유.csv"
cat.to_csv(filename, encoding='cp949', index=False)
