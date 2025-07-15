# 📚 Library AI - Data Fetcher

이 프로젝트는 공공 도서관 대출 데이터를 수집하기 위한 Python 스크립트입니다.  
`data4library` 공공 API를 사용하여 최근 12개월간의 도서 대출 데이터를 수집하고 CSV 파일로 저장할 수 있습니다.

---

## 📦 주요 기능

- 📅 최근 12개월간 월별 도서 대출 데이터 수집
- 🧾 제목, 저자, 출판사, KDC 분류번호 추출
- 📂 Pandas를 이용한 DataFrame 생성 및 CSV 저장 가능

---

## ⚙️ 설치 및 실행 방법

### 1. 환경 세팅

```bash
git clone https://github.com/yourusername/libraryAI.git
cd libraryAI
pip install -r requirements.txt


2. .env 파일 생성
ini
복사
편집
# .env
API_KEY=발급받은_API_키
LIB_CODE=도서관_코드
.env는 Git에 업로드되지 않도록 .gitignore로 제외되어 있어야 합니다.

3. 실행
bash
복사
편집
python data_fetcher.py
실행 시, loan_books.csv 파일이 생성됩니다.



📁 프로젝트 구조
bash
복사
편집
libraryAI/
├── data_fetcher.py        # 데이터 수집 및 전처리 로직
├── loan_books.csv         # 수집된 데이터 CSV 파일 (실행 후 생성됨)
├── requirements.txt       # 의존성 목록
├── .env                   # API 키 및 도서관 코드 (Git에 포함되지 않음)
└── README.md              # 프로젝트 설명 파일

📌 향후 계획
Streamlit을 이용한 시각화 및 추천 기능 추가

사용자 선택 기반 라이브러리 연동
