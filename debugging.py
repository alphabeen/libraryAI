import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json

# 환경변수 불러오기
load_dotenv()
API_KEY = os.getenv("API_KEY")
LIB_CODE = os.getenv("LIB_CODE")

# 📌 단일 월간 데이터 요청 (디버깅용)
def fetch_monthly_data_debug(start, end):
    url = (
        f"http://data4library.kr/api/itemSrch?"
        f"libCode={LIB_CODE}&startDt={start}&endDt={end}"
        f"&authKey={API_KEY}&format=json"
    )
    print(f"\n📡 요청 URL:\n{url}\n")

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ 요청 실패: status code {response.status_code}")
        return pd.DataFrame()

    try:
        data = response.json()
        print(f"📦 응답 JSON 일부:\n{json.dumps(data, indent=2, ensure_ascii=False)[:1000]}...\n")
    except Exception as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return pd.DataFrame()

    items = data.get("response", {}).get("docs", [])

    if not items:
        print("⚠️ docs 데이터 없음")
    else:
        print(f"✅ docs 항목 수: {len(items)}")

    # 🔍 각 doc 내부 구조 확인
    for i, doc in enumerate(items[:3]):  # 최대 3개만 출력
        print(f"\n🔍 doc[{i}] 전체:\n{json.dumps(doc, indent=2, ensure_ascii=False)}")
        print(f"🔑 doc[{i}].keys(): {doc.keys()}")
        if "book" in doc:
            print(f"📘 book keys: {doc['book'].keys()}")
        else:
            print("❗ book 키 없음!")

    # 📊 실제 DataFrame 생성
    records = []
    for doc in items:
        book_info = doc.get("book", {})
        records.append({
            "제목": book_info.get("bookname"),
            "저자": book_info.get("authors"),
            "출판사": book_info.get("publisher"),
            "KDC": book_info.get("class_no")
        })

    df = pd.DataFrame(records)
    print("\n📋 DataFrame 미리보기:")
    print(df.head())
    return df

# ✅ 최근 1개월 테스트 실행
if __name__ == "__main__":
    today = datetime.today()
    end = today.strftime("%Y-%m-01")
    start = (today - timedelta(days=30)).strftime("%Y-%m-01")
    fetch_monthly_data_debug(start, end)
