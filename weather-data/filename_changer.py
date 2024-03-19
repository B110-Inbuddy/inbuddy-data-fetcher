import time
import pandas as pd
import os

TEST = False
PATH = "C:/Users/SSAFY/weather-data/data"

path = PATH + ("_test" if TEST else "")
files = os.listdir(path)

for file in files:
    print("* " + file)

    if not file.endswith(".csv"):
        print("*** " + file + " is not an csv file. skip")
        continue

    df = pd.read_csv(path + '/' + file, encoding='cp949', header=None, skiprows=1)
    date = df.loc[0, 1]

    # 새로운 파일 이름 생성
    new_file_name = date[:4] + date[5:7] + '_' + str(time.time()) + '.csv'
    # print(new_file_name)

    # 파일 이름 변경
    os.rename(path + '/' + file, os.path.join(os.path.dirname(path + '/' + file), new_file_name))
