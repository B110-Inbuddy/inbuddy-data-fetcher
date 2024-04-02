import time

import pandas as pd
import os

TEST = True
PATH = "C:/Users/SSAFY/flights-data/data"

path = PATH + ("_test" if TEST else "")
files = os.listdir(path)

print('*' * 50)
print('import path: ', path)
print('import files: ', files)

# COLUMNS = {
#     'D': ["날짜", "항공사", "편명", "도착지", "계획", "예상", "실제", "구분", "현황", "사유"],
#     'A': ["날짜", "항공사", "편명", "출발지", "계획", "예상", "실제", "구분", "현황", "사유"]
# }

COLUMNS = {
    'D': ["departure_date", "airline", "flight_code", "destination", "departure_time_plan", "departure_time_expexted", "departure_time_real", "division", "flight_status", "cause"],
    'A': ["arrival_date", "airline", "flight_code", "origin", "arrival_time_plan", "arrival_time_expexted", "arrival_time_real", "division", "flight_status", "cause"]
}


cat_arrive = pd.DataFrame(columns=COLUMNS['A'])
cat_departure = pd.DataFrame(columns=COLUMNS['D'])

### 디렉터리 생성
print("*" * 50)
print("check data directory")

if not os.path.isdir(path + '/data'):
    os.mkdir(path + '/data')
    print("new data directory created")

### concatenation 시작
print('*' * 50)
print("start concatenation")

START_DATE = '99999999'
END_DATE = '00000000'

for file in files:
    print("* " + file)
    if not file.endswith(".csv"):
        print("*** " + file + " is not an csv file. skip")
        continue

    if len(file) < 9 or file[8] not in ['A', 'D']:
        print("*** Filename of " + file + " is incorrect. skip")
        continue

    file_type = file[8]  # 'A' 또는 'D'
    df = pd.read_csv(path + '/' + file, encoding='cp949', header=None, skiprows=1, names=COLUMNS[file_type])

    # df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
    df = df[df['division'] != '화물']
    
    START_DATE = min(START_DATE, file[:8])
    END_DATE = max(END_DATE, file[:8])

    if file[8] == 'A':
        cat_arrive = pd.concat([cat_arrive, df], ignore_index=True)
    else:
        cat_departure = pd.concat([cat_departure, df], ignore_index=True)

print("concatenation completed")
print(cat_arrive.head(10))

print("*" * 50)
print("set column names")

cat_arrive.columns = COLUMNS['A']
cat_departure.columns = COLUMNS['D']

print("*" * 50)
print("sort by date, time")


# cat_arrive.sort_values(by=['날짜', '계획'], ascending=[True, True], inplace=True)
# cat_departure.sort_values(by=['날짜', '계획'], ascending=[True, True], inplace=True)

cat_arrive.sort_values(by=['arrival_date', 'arrival_time_plan'], ascending=[True, True], inplace=True)
cat_departure.sort_values(by=['departure_date', 'departure_time_plan'], ascending=[True, True], inplace=True)


# cat_arrive = cat_arrive.drop_duplicates().reset_index(drop=True)
# cat_departure = cat_departure.drop_duplicates().reset_index(drop=True)

cat_arrive.reset_index(inplace=True)
cat_departure.reset_index(inplace=True)

cat_arrive['index'] = cat_arrive['index'] + 1
cat_departure['index'] = cat_departure['index'] + 1


cat_arrive.rename(columns={'index': 'flight_info_id'}, inplace=True)
cat_departure.rename(columns={'index': 'flight_info_id'}, inplace=True)


def filename(dep_arr):
    return START_DATE + '-' + END_DATE + dep_arr + str(time.time()) + '.csv'


filepath = path + "/data/" + filename('A')
cat_arrive.to_csv(filepath, encoding='cp949', index=False)
print("new " + filepath + " created")

filepath = path + "/data/" + filename('D')
cat_departure.to_csv(filepath, encoding='cp949', index=False)
print("new " + filepath + " created")
