import os
import requests
import pandas as pd
import time
import zipfile
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
LIB_CODE = os.getenv("LIB_CODE")
BASE_URL = os.getenv("BASE_URL")

def fetch_popular_books(start, end, age=None, gender=None, region=None, kdc=None, page_size=100, max_pages=50):
    records = []
    page = 1

    while page <= max_pages:
        params = {
            "authKey": API_KEY,
            "startDt": start,
            "endDt": end,
            "format": "json",
            "pageNo": page,
            "pageSize": page_size,
        }

        if age:
            params["age"] = age
        if gender:
            params["gender"] = gender
        if region:
            params["region"] = region
        if kdc:
            params["kdc"] = kdc

        print(f"Fetching: {start} ~ {end}, page {page}") #디버깅용

        try:
            response = requests.get(BASE_URL, params=params)
            items = response.json().get("response", {}).get("docs", [])
        except Exception as e:
            print("응답 파싱 오류:", e)
            break

        if not items:
            print("더 이상 데이터가 없음")
            break

        for doc in items:
            book = doc.get("doc", {})
            records.append({
                "순위": book.get("ranking"),
                "도서명": book.get("bookname"),
                "저자": book.get("authors"),
                "출판사": book.get("publisher"),
                "출판년도": book.get("publication_year"),
                "ISBN": book.get("isbn13"),
                "KDC": book.get("class_no"),
                "KDC명": book.get("class_nm"),
                "대출건수": book.get("loan_count")
            })

        page += 1
        time.sleep(0.3)  # API 호출 간 딜레이

    return pd.DataFrame(records)

def fetch_last_12_months(age=None, gender=None, region=None, kdc=None, save_dir="month_data"):
    os.makedirs(save_dir, exist_ok=True)
    today = datetime.today().replace(day=1) #월 초 설정
    dfs = []

    for i in range(12):
        start = (today - relativedelta(months=i + 1)).strftime("%Y-%m-%d")
        end = (today - relativedelta(months=i)).strftime("%Y-%m-%d")
        filename = f"{save_dir}/popular_books_{start[:7]}.csv"
        
        if os.path.exists(filename):
            print(f"이미 존재: {filename}, 건너뜀")
            continue

        df = fetch_popular_books(
            start=start,
            end=end,
            age=age,
            gender=gender,
            region=region,
            kdc=kdc,
            max_pages=50
        )
        if not df.empty:
            dfs.append(df)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"저장 완료: {filename}")
        else:
            print(f"빈 데이터: {start[:7]}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def zip_monthly_csvs(directory="month_data", zip_name="month_books.zip"):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                zipf.write(file_path, arcname=filename)
    print(f"압축 완료: {zip_name}")

if __name__ == "__main__":
    df = fetch_last_12_months(age="20", gender="1", region="11", kdc=None)  
    # 예: 20대 남성 서울 -> 나중에 파라미터로 조절 가능
    df.to_csv("popular_books_last_12_months.csv", index=False)
    print("인기대출도서 데이터 저장 완료")
    print(df.head())
    zip_monthly_csvs()  # 월별 CSV 파일 압축