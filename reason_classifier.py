import os
import pandas as pd

TEST = False
PATH = "C:/Users/SSAFY/flights-data/data/data"

path = PATH + ("_test" if TEST else "")

df = pd.read_csv("항공기도착현황_20070101-20240307.csv")




