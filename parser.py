import os
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

PATH = "C:/Users/oh382/Downloads"
DATE = "20070505"

PARAMS = {
    "gubun": "c_getList",
    "depArr": "A",
    "current_date": DATE,
    "airport": "RKSI",
    "al_icao": "",
    "fp_id": ""
}

DOMAIN = "https://www.airportal.go.kr/life/airinfo/RbHanList.jsp"

URL = DOMAIN + '?' + '&'.join(
        [f"{key}={value}" for key, value in PARAMS.items()])

response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

indent_one = soup.select("FORM > table > tr > TD > table > tr > td")
indent_two = soup.select("FORM > table > tr > TD > table > td")
tds = soup.select("FORM > table > td")

PREFIX = "ddrivetip('"
SUFFIX = "에 의한 지연'"

columns = ["항공사", "편명", "출발지", "계획", "예상", "도착", "구분", "현황", "지연사유"]

cat = pd.DataFrame(columns=columns)


def extract(row):
    global cat
    list = []
    for index in range(0, len(row), 2):
        string = str(row[index])
        c = BeautifulSoup(string, 'html.parser')
        text = c.text.strip()
        list.append(text)

        if index == 14:
            list.append(string[string.find(PREFIX) + len(PREFIX):string.find(
                SUFFIX)] if text == '지연' else '')

    print(list)
    cat.loc[len(cat)] = list


extract(indent_one)
extract(indent_two)

for index in range(0, len(tds), 15):
    extract(tds[index:index + 15])

print(cat.head(5))

if not os.path.exists(PATH + '/data'):
    os.mkdir(PATH + '/data')
elif not os.path.isdir(PATH + '/data'):
    os.remove(PATH + '/data')
    os.mkdir(PATH + '/data')


cat = cat.reset_index(drop=True)

cat.to_csv(PATH + '/data/data' + DATE + '.' + str(time.time()) + '.csv', encoding='cp949', index=False)

print("new data.csv file created. length: ", len(cat))

# print("indent one: ", indent_one)
# print("indent two[0]: ", indent_two[0])
# print("tds[0]: ", tds[0])

# s = BeautifulSoup(str(indent_one[0]), 'html.parser')
# print(s.text)

# print("test: ", s.get('width'))

# for td, index in tds:
#     print(f"index: {index}\t{td.text.trim()}")
