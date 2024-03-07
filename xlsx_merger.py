import pandas as pd
import os
import time
import shutil
import warnings
warnings.filterwarnings("ignore")

TEST = False
DOWNLOADED_PATH = "C:/Users/SSAFY/Downloads/flights"

path = DOWNLOADED_PATH + ("_test" if TEST else "")

print('*' * 50)
print('import path: ', path)


files = os.listdir(path) # xlsx 만 불러오게 수정
print('import files: ', files)

if not os.path.isdir(path + '/merged'):
    os.mkdir(path + '/merged')
    print("* merged directory created")

# "출/도착구분    날짜    항공사    편명    출발공항코드    출발공항명    도착공항코드    도착공항명    계획시간    예상시간    출발시간    구분    현황".split('\t')

cat = pd.DataFrame(columns=[i for i in range(13)])
error_files = []


print('*' * 50)
print("start concatenation")


for file in files:
    print("* " + file)
    if not file.endswith(".xlsx"):
        print("*** " + file + " is not an excel file. skip")
        continue

    df = pd.read_excel(path + '/' + file, engine='openpyxl', header=None, skiprows=1)

    if df.empty:
        print("*** " + file + " is empty. skip")
        error_files.append(file[:9])
        os.remove(path + '/' + file)
        print("*** " + file + " deleted")
        continue

    # print("df: ", df.head(3))

    row = df.iloc[0]
    # print("row: ", row)

    content_status = str(row[0]).strip() # '출발' 또는 '도착'
    content_date = str(row[1]).strip() # yyyymmdd
    content_yyyymm = content_date[:6].strip() # yyyymm

    title_yyyymm = file[:6].strip() # yyyymm
    title_status = '출발' if file[6:9] == 'Arr' else '도착' # '출발' 또는 '도착'

    if content_status != title_status and content_yyyymm != title_yyyymm:
        print("*** " + file + " does not match with its content. skip")
        error_files.append(file)
        os.remove(path + '/' + file)
        print("*** " + file + " deleted")
        continue

    cat = pd.concat([cat, df], ignore_index=True, axis=0)

    shutil.move(path + '/' + file, path + '/merged/' + file)

print("concatenation completed")

print("*" * 50)
print("create data directory")

if not os.path.isdir(path + '/data'):
    # print("* old data directory removed")
    os.mkdir(path + '/data')
    print("new data directory created")

    # shutil.rmtree(path + '/data')



print("*" * 50)
print("create data.csv file")

cat.columns = ['출/도착구분', '날짜', '항공사', '편명', '출발공항코드', '출발공항명', '도착공항코드', '도착공항명', '계획시간', '예상시간', '출발시간', '구분', '현황']
if cat.empty:
    print("*** result has no data. skip")

else:
    cat.to_csv(path + '/data/data' + str(time.time()) + '.csv', encoding='cp949')
    print("new data.csv file created")

print("*" * 50)
print("create error directory")

if os.path.isdir(path + '/error'):
    print("* old error directory removed")
    shutil.rmtree(path + '/error')

os.mkdir(path + '/error')
print("new error directory created")

print("*" * 50)
print("create error.txt file")

with open(path + '/error/errors.txt', 'w+') as file:
    file.write('\n'.join(error_files))
print("new error.txt file created")


print("DONE")