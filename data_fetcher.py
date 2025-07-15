import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
LIB_CODE = os.getenv("LIB_CODE")

def fetch_monthly_data(start, end):
    url = f"http://data4library.kr/api/itemSrch?libCode={LIB_CODE}&startDt={start}&endDt={end}&authKey={API_KEY}&format=json"
    response = requests.get(url)
    items = response.json().get("response", {}).get("docs", [])
    
    records = []
    for doc in items:
        book_info = doc.get("doc", {})
        records.append({
            "제목": book_info.get("bookname"),
            "저자": book_info.get("authors"),
            "출판사": book_info.get("publisher"),
            "KDC": book_info.get("class_no")
        })
    return pd.DataFrame(records)

def fetch_last_12_months():
    today = datetime.today()
    dfs = []
    for i in range(12):
        end = (today - timedelta(days=30 * i)).strftime("%Y-%m-01")
        start = (today - timedelta(days=30 * (i + 1))).strftime("%Y-%m-01")
        df = fetch_monthly_data(start, end)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

df = fetch_last_12_months()
print(df.head())
df.to_csv("loan_books.csv", index=False, encoding="utf-8-sig")
