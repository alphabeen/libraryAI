import pandas as pd
 
def preprocess_csv(input_path="loan_books.csv", output_path="cleaned_books.csv"):
    df = pd.read_csv(input_path, encoding='utf-8-sig')
    print(f"원본 데이터 크기: {df.shape}")

    # 1. 결측치 제거
    df.dropna(subset=["제목", "저자", "출판사", "KDC"], inplace=True)
    # 2. KDC 앞 세 자리만 추출
    df["KDC"] = df["KDC"].astype(str).str.extract(r"(\d{3})")

    # 3. 문자열 정제 (공백 제거)
    for col in ["제목", "저자", "출판사"]:
        df[col] = df[col].astype(str).str.strip()

    # 4. 중복 제거
    df.drop_duplicates(inplace=True)

    print(f" 전처리 후 데이터 크기: {df.shape}")

    # 5. 저장
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"전처리 완료, 저장 위치: {output_path}")

if __name__ == "__main__":
    preprocess_csv()