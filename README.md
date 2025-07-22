# 📚 Library AI - Data Fetcher

## 📌 목표
- 국립중앙도서관 "인기대출도서 조회 API"를 활용하여 최근 12개월간 월별 도서 데이터를 수집하고, 자동으로 CSV로 저장 및 압축하는 파이프라인 구축
- 사용자별 인기도서를 수준에 맞게 추천해주는 기계학습 구축 (예정)

---
## 실행내역

### 1. 도서 대출 데이터 수집 스크립트 개발 (`data_fetcher.py`)
- `.env` 환경변수 기반 API 키 및 기본 설정 관리
- `fetch_popular_books()` 함수 작성
  - 단일 기간(`start`~`end`)에 대해 인기 도서 데이터를 최대 50페이지까지 수집
  - 파라미터: 연령대, 성별, 지역, KDC 분류 지원
  - 결과는 pandas `DataFrame`으로 반환

- `fetch_last_12_months()` 함수 작성
  - 오늘 날짜 기준으로 최근 12개월에 대한 데이터를 월 단위로 순차 수집
  - 월별로 `.csv` 파일 자동 저장 (`month_data/` 디렉토리)
  - 이미 저장된 월은 재요청하지 않고 건너뜀 (캐싱 효과)

---

### 2. 성능 및 예외 처리 개선
- API 호출 간 `time.sleep(0.3)`으로 요청 제한 회피
- 응답 파싱 오류 예외 처리 추가
- 빈 응답 데이터에 대한 경고 출력

---

### 3. 월별 CSV 파일 자동 압축 기능 추가
- `zip_monthly_csvs()` 함수 작성
  - `month_data/` 폴더의 `.csv` 파일을 하나의 `.zip` 파일(`monthly_books.zip`)로 압축
  - 압축 완료 메시지 출력

- `__main__` 실행부에 통합
  - 전체 12개월 데이터 `.csv` 저장
  - 월별 `.csv` → `monthly_books.zip` 압축 자동 수행

---

## 사용자 흐름(User flow)
1. 앱 실행 (streamlit UI)
2. 관심 주제 선택 or 입력 (ex. "로맨스", "과학", "인공지능" etc..)
3. 추천 버튼 클릭 -> 백엔드에 전달
4. 결과 확인 -> 관련 도서 keyword + 추천 책 목록 출력

## Backend Architecture
1. API 호출(data_fetcher.py) -> 도서 대출 데이터 수집(monthly_books.zip)
2. 데이터 저장
3. 전처리(preprocess.py) -> KDC별 도서 제목 정제, 형태소 분석
4. 키워드 추출(keyword_extractor.py) ->  TF-IDF + TextRank 기반 핵심 키워드 추출
5. 추천 로직(recommender.py) -> KDC별 추천 로직 (예정)
5. 결과 저장

---
## ⚙️ 설치 및 실행 방법

### 1. 환경 세팅

```bash
git clone https://github.com/alphabeen/libraryAI.git
cd libraryAI
pip install -r requirements.txt


2. .env 파일 생성
# .env
API_KEY=발급받은_API_키
LIB_CODE=도서관_코드
BASE_URL=https://api.nl.go.kr/libsrch/loan/popular
.env는 Git에 업로드되지 않도록 .gitignore로 제외되어 있어야 합니다.

3. 실행
python data_fetcher.py
실행 시, `month_data/` 에 월별 `.csv` 파일 생성
popular_books_last_12_months.csv로 통합 저장
monthly_books.zip 압축본 자동 생성

📁 프로젝트 구조
libraryAI/
├── .env                     # API_KEY, LIB_CODE 등
├── .gitignore              # .env, __pycache__ 제외
├── data_fetcher.py         # 데이터 수집 
├── popular_books_last_12_months.csv #전체 통합 데이터
├── monthly_books.zip       # 12개월 월별 파일 압축본
└── month_data/             # 매 달 인기대출데이터 수집
├── popular_books_2024-07.csv
├── ...
└── popular_books_2025-06.csv
├── preprocess.py           # 형태소 분석 등 전처리 모듈 (예정)
├── keyword_extractor.py    # TF-IDF + TextRank 분석
├── recommender.py          # (예정) KDC 기반 추천 로직
├── streamlitapp.py         # (예정) UI 로직
├── requirements.txt    #필요 패키지 목록록
└── README.md          # 프로젝트 설명 파일
```


🚀 향후 개발 계획
 사용자 관심 키워드 기반 도서 추천 기능 강화

 KDC 분류별 추천 알고리즘 고도화

 Streamlit 기반 시각화 대시보드 구축

 연령/성별/지역 조건 필터링 UI 연동

 학습용 모델로 키워드 트렌드 예측 기능 실험