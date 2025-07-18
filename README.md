# 📚 Library AI - Data Fetcher

이 프로젝트는 공공 도서관 대출 데이터를 수집하기 위한 Python 스크립트입니다.  
`data4library` 공공 API를 사용하여 최근 12개월간의 도서 대출 데이터를 수집하고 CSV 파일로 저장할 수 있습니다.

---

## 📦 주요 기능

- 📅 최근 12개월간 월별 도서 대출 데이터 수집
- 🧾 제목, 저자, 출판사, KDC 분류번호 추출
- 📂 Pandas를 이용한 DataFrame 생성 및 CSV 저장 가능

## 사용자 흐름(User flow)
1. 앱 실행 (streamlit UI)
2. 관심 주제 선택 or 입력 (ex. "로맨스", "과학", "인공지능" etc..)
3. 추천 버튼 클릭 -> 백엔드에 전달
4. 결과 확인 -> 관련 도서 keyword + 추천 책 목록 출력

## Backend Architecture
1. API 호출(data_fetcher.py) -> 도서 대출 데이터 수집(loan_books.csv)
2. 데이터 저장
3. 전처리(preprocess.py) -> KDC별 도서 제목 정제, 형태소 분석
4. 키워드 추출(recommender.py) -> KDC별 상위 핵심 키워드 추출 및 정렬
5. 결과 저장

---
## ⚙️ 설치 및 실행 방법

### 1. 환경 세팅

```bash
git clone https://github.com/yourusername/libraryAI.git
cd libraryAI
pip install -r requirements.txt


2. .env 파일 생성
# .env
API_KEY=발급받은_API_키
LIB_CODE=도서관_코드
.env는 Git에 업로드되지 않도록 .gitignore로 제외되어 있어야 합니다.

3. 실행
python data_fetcher.py
실행 시, loan_books.csv 파일이 생성됩니다.

📁 프로젝트 구조
libraryAI/
├── .env                     # API_KEY, LIB_CODE 등
├── .gitignore              # .env, __pycache__ 제외
├── loan_books.csv          # 원본 데이터
├── cleaned_books.csv       # 전처리된 데이터
├── data_fetcher.py         # API 호출 및 수집
├── keyword_extractor.py    # TF-IDF + TextRank 분석
├── recommender.py          # (예정) KDC 기반 추천 로직
├── streamlitapp.py         # (예정) UI 로직
├── requirements.txt
└── README.md          # 프로젝트 설명 파일
```

📌 향후 계획
Streamlit을 이용한 시각화 및 추천 기능 추가

사용자 선택 기반 라이브러리 연동
