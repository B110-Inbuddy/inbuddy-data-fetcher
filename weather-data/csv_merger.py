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

COLUMNS = ["지점", "일시", "기온(°C)", "10분평균풍속(KT)", "10분평균풍향(deg)", "10분평균MOR(m)", "10분평균RVR(m)", "누적강수량(mm)"]

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

cat.sort_values(by=['일시'], ascending=True, inplace=True)

cat = cat.drop_duplicates().reset_index(drop=True)


def filename():
    return '인천공항기상현황_'+'200701'+'-'+'20240319' + '_'+ str(time.time()) + '.csv'


filepath = path + "/data/" + filename()
cat.to_csv(filepath, encoding='cp949', index=False)
print("new " + filepath + " created")


