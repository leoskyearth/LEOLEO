import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 파일 업로드 함수
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error: {e}")
    return None

# 메인 함수
def main():
    st.title('뉴스 대시보드')

    # 파일 업로더 추가
    uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type="csv")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # 사이드바: 필터링 옵션
            st.sidebar.header('필터링 옵션')
            keyword = st.sidebar.text_input('키워드로 필터링:')

            # 키워드로 필터링
            if keyword:
                df = df[df['Title'].str.contains(keyword, case=False)]

            # 메인 화면: 데이터 표시
            st.header('뉴스 목록')
            st.dataframe(df)

            # 뉴스 제목 길이 분석
            st.header('뉴스 제목 길이 분석')
            df['Title_Length'] = df['Title'].str.len()
            fig = px.histogram(df, x='Title_Length', nbins=20, title='뉴스 제목 길이 분포')
            st.plotly_chart(fig)

            # 개별 뉴스 상세 정보
            st.header('개별 뉴스 상세 정보')
            selected_news = st.selectbox('뉴스 선택:', df['Title'])
            if selected_news:
                news_info = df[df['Title'] == selected_news].iloc[0]
                st.subheader(news_info['Title'])
                st.write(f"링크: {news_info['Link']}")
    else:
        st.info("CSV 파일을 업로드해주세요.")

if __name__ == '__main__':
    main()