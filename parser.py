import os
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

PATH = "C:/Users/SSAFY/flights-data"

DOMAIN = "https://www.airportal.go.kr/life/airinfo/RbHanList.jsp"

COLUMNS = ["날짜", "항공사", "편명", "출발지", "계획", "예상", "도착", "구분", "현황", "지연사유"]

PREFIX = "ddrivetip('"
SUFFIX = "에 의한 지연'"


def request(date, dep_arr):
    def extract(row):
        row_data = [date]
        for index in range(0, len(row), 2):
            string = str(row[index])
            c = BeautifulSoup(string, 'html.parser')
            text = c.text.strip()
            row_data.append(text)

            if index == 14:
                row_data.append(
                        string[string.find(PREFIX) + len(PREFIX):string.find(
                                SUFFIX)] if text == '지연' else '')
        # print(row_data)
        return row_data

    cat = pd.DataFrame(columns=COLUMNS)
    params = {
        "gubun": "c_getList",
        "depArr": dep_arr,
        "current_date": date,
        "airport": "RKSI",
        "al_icao": "",
        "fp_id": ""
    }

    url = DOMAIN + '?' + '&'.join(
            [f"{key}={value}" for key, value in params.items()])

    # request
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    indent_one = soup.select("FORM > table > tr > TD > table > tr > td")
    indent_two = soup.select("FORM > table > tr > TD > table > td")
    tds = soup.select("FORM > table > td")

    # append rows
    cat.loc[len(cat)] = extract(indent_one)
    cat.loc[len(cat)] = extract(indent_two)
    for index in range(0, len(tds), 15):
        cat.loc[len(cat)] = extract(tds[index:index + 15])

    cat = cat.reset_index(drop=True)

    # create csv
    filename = f"{PATH}/data/{date}{dep_arr}.{str(time.time())}.csv"
    cat.to_csv(filename, encoding='cp949', index=False)

    print(cat.head(5))
    print("new data.csv file created. length: ", len(cat))


def init():
    if not os.path.exists(PATH + '/data'):
        os.mkdir(PATH + '/data')
    elif not os.path.isdir(PATH + '/data'):
        os.remove(PATH + '/data')
        os.mkdir(PATH + '/data')

    start_date = datetime(2017, 1, 1)
    end_date = datetime(2017, 1, 2)

    date = start_date
    while date <= end_date:
        formatted = date.strftime("%Y%m%d")
        print(formatted)
        request(formatted, 'D')
        request(formatted, 'A')

        date += timedelta(days=1)


init()
