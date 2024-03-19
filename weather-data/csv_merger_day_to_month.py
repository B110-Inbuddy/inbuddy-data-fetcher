import shutil
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

COLUMNS = ["지점", "지점명", "일시", "기온(°C)", "10분평균풍속(KT)", "10분평균풍향(deg)", "10분평균MOR(m)", "10분평균RVR(m)", "누적강수량(mm)"]

cat = pd.DataFrame(columns=[i for i in range(9)])

### 디렉터리 생성
print("*" * 50)
print("check data directory")

if not os.path.isdir(path + '/data'):
    os.mkdir(path + '/data')
    print("new data directory created")

### concatenation 시작
print('*' * 50)
print("start concatenation")

YYYYMM = '202105'
merged_files = []

for file in files:
    print("* " + file)

    if not file.endswith(".csv"):
        print("*** " + file + " is not an csv file. skip")
        continue

    df = pd.read_csv(path + '/' + file, encoding='cp949', header=None, skiprows=1)
    date = df.loc[0, 2]
    if date[:4] + date[5:7] != YYYYMM:
        print("*** " + file + " is not matched. skip")
        continue

    cat = pd.concat([cat, df], ignore_index=True)
    merged_files.append(file)

print("concatenation completed")
print(cat.head(10))

print("*" * 50)
print("set column names")
cat.columns = COLUMNS

print("*" * 50)
print("sort by date")
cat.sort_values(by=['일시'], ascending=True, inplace=True)

cat = cat.drop_duplicates().reset_index(drop=True)


def filename():
    date = cat.loc[0, '일시']
    return date[:4] + date[5:7] + '_' + str(time.time()) + '.csv'


filepath = path + "/data/" + filename()
cat.to_csv(filepath, encoding='cp949', index=False)
print("new " + filepath + " created")

# 새로운 파일이 생성된 후 해당 파일을 'merged' 폴더로 이동하고 원본 파일을 삭제
if not os.path.exists(os.path.join(path, "merged")):
    os.mkdir(os.path.join(path, "merged"))

# 원본 파일을 'merged' 폴더로 이동
for file in merged_files:
    if file.endswith(".csv"):
        shutil.move(os.path.join(path, file), os.path.join(path, "merged", file))
        print("Moved", file, "to 'merged' folder")
