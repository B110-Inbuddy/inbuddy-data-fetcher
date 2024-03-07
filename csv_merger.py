import pandas as pd
import os

TEST = False
PATH = "C:/Users/SSAFY/Downloads/flights/data"

path = PATH + ("_test" if TEST else "")
files = os.listdir(path)

columns = ['출/도착구분', '날짜', '항공사', '편명', '출발공항코드', '출발공항명', '도착공항코드', '도착공항명', '계획시간', '예상시간', '출발시간', '구분', '현황']

df_all_data = pd.DataFrame(columns=columns)

for file in files:
    if file.endswith(".csv"):
        df = pd.read_csv(path + '/' + file, encoding='cp949', index_col=0)
        df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
        df_all_data = pd.concat([df_all_data, df], ignore_index=True)

print(df_all_data.head(10))

df_all_data.sort_values(by=['날짜', '출/도착구분', '계획시간'], ascending=[True, False, True], inplace=True)
df_all_data = df_all_data.drop_duplicates().reset_index(drop=True)

df_all_data.to_csv(path + "/" + "all_data.csv", encoding='cp949')
print("all_data created")
