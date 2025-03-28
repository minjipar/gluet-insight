import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="글루어트 인스타그램 키워드 보드", layout="wide")
st.title("🧃 글루어트 인스타그램 키워드 인사이트 보드")

# 버튼으로 크롤링 트리거
if st.button("🔄 인스타그램 게시물 다시 수집하기"):
    os.system("python instagram_crawler.py")
    st.success("크롤링 완료! 최신 게시물로 업데이트되었습니다.")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("posts.csv")

try:
    df = load_data()
    df["date"] = pd.to_datetime(df["date"])

    # 날짜 필터
    st.sidebar.title("📅 날짜 필터")
    start = st.sidebar.date_input("시작일", df['date'].min().date())
    end = st.sidebar.date_input("종료일", df['date'].max().date())
    filtered = df[(df['date'] >= pd.to_datetime(start)) & (df['date'] <= pd.to_datetime(end))]

    # 인기 키워드 추출
    st.subheader("🔥 인기 키워드")
    keywords = pd.Series(" ".join(filtered["caption"]).split()).value_counts().head(10)
    st.write(keywords)

    # 테이블
    st.subheader("📄 게시물 목록")
    for _, row in filtered.iterrows():
        st.markdown(f"**{row['date']}**  
{row['caption']}  
[🔗 인스타그램 링크]({row['link']})")
        st.image(row['image'], width=150)
        st.markdown("---")

    # 다운로드
    st.download_button("📥 CSV 다운로드", filtered.to_csv(index=False), "gluort_posts.csv")

except Exception as e:
    st.warning("데이터를 불러올 수 없습니다. 먼저 게시물을 수집해주세요.")
