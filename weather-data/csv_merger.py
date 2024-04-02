import time

import pandas as pd
import os

TEST = False
PATH = "C:/Users/SSAFY/weather-data/data"

path = PATH + ("_test" if TEST else "")
files = os.listdir(path)

print('*' * 50)
print('import path: ', path)
print('import files: ', files)

# COLUMNS = ["지점", "일시", "기온(°C)", "10분평균풍속(KT)", "10분평균풍향(deg)", "10분평균MOR(m)", "10분평균RVR(m)", "누적강수량(mm)"]
COLUMNS = ["point", "weather_date", "temperature", "wind_speed_10m_avg_kt", "wind_dir_10m_avg_deg", "mor_10m_avg_m",
           "rvr_10m_avg_m", " cumulative_precipitation_mm"]

cat = pd.DataFrame(columns=[i for i in range(8)])

### 디렉터리 생성
print("*" * 50)
print("check data directory")

if not os.path.isdir(path + '/data'):
    os.mkdir(path + '/data')
    print("new data directory created")

### concatenation 시작
print('*' * 50)
print("start concatenation")

for file in files:
    print("* " + file)

    if not file.endswith(".csv"):
        print("*** " + file + " is not an csv file. skip")
        continue

    df = pd.read_csv(path + '/' + file, encoding='cp949', header=None, skiprows=1)

    # df['일시'] = pd.to_datetime(df['일시'], format='%Y%m%d')
    cat = pd.concat([cat, df], ignore_index=True)

print("concatenation completed")
print(cat.head(10))

print("*" * 50)
print("set column names")

cat.columns = COLUMNS

print("*" * 50)
print("sort by date, time")

# cat.sort_values(by=['일시'], ascending=True, inplace=True)
cat.sort_values(by=['weather_date'], ascending=True, inplace=True)

# cat = cat.drop_duplicates().reset_index(drop=True)

cat.reset_index(inplace=True)
cat['index'] = cat['index'] + 1
cat.rename(columns={'index': 'weather_id'}, inplace=True)


def filename():
    START_DATE = cat['weather_date'].min()
    START_DATE = START_DATE[:4]+START_DATE[5:7]+START_DATE[8:10]
    END_DATE = cat['weather_date'].max()
    END_DATE = END_DATE[:4]+END_DATE[5:7]+END_DATE[8:10]


    return '인천공항기상현황_' + START_DATE + '-' + END_DATE + '_' + str(time.time()) + '.csv'


filepath = path + "/data/" + filename()
print(filepath)
cat.to_csv(filepath, encoding='cp949', index=False)
print("new " + filepath + " created")
