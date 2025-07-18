import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import networkx as nx # type: ignore
from konlpy.tag import Okt

# 파일 불러오기
df = pd.read_csv("cleaned_books.csv", encoding='utf-8-sig')
df = df.dropna(subset=["제목", "KDC"])

# 형태소 분석기 준비
okt = Okt()

# KDC별로 제목 텍스트를 합침
grouped = df.groupby("KDC")["제목"].apply(lambda titles: " ".join(titles))

# 최종 결과 저장
final_keywords = {}

# KDC 그룹별 처리
for kdc, text in grouped.items():
    # 1. 형태소 추출 및 명사 필터링
    nouns = okt.nouns(text)
    filtered_words = [word for word in nouns if len(word) > 1]

    # 2. TF-IDF 벡터화
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(filtered_words)])
    tfidf_scores = dict(zip(tfidf_vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))

    # 3. TextRank를 위한 co-occurrence 그래프 구축
    graph = nx.Graph()
    window_size = 4
    for i in range(len(filtered_words) - window_size + 1):
        window = filtered_words[i:i+window_size]
        for w1 in window:
            for w2 in window:
                if w1 != w2:
                    graph.add_edge(w1, w2, weight=graph.get_edge_data(w1, w2, {}).get("weight", 0) + 1)

    # 4. TextRank 점수 계산
    textrank_scores = nx.pagerank(graph, weight='weight')

    # 5. TF-IDF와 TextRank 결합
    combined_scores = {}
    for word in set(filtered_words):
        tfidf = tfidf_scores.get(word, 0)
        textrank = textrank_scores.get(word, 0)
        combined_scores[word] = tfidf * textrank

    # 6. 상위 키워드 추출
    top_keywords = Counter(combined_scores).most_common(5)
    final_keywords[kdc] = top_keywords

# 결과 출력
result_df = pd.DataFrame([
    {"KDC": kdc, "Keyword": kw, "Score": round(score, 4)}
    for kdc, keywords in final_keywords.items()
    for kw, score in keywords
])
print(result_df)
