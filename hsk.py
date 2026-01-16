import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="10월 수산물 무역 리포트", layout="wide")

FILE_NAME = '해양수산부_HSK품목별수출입현황_20251031.csv' 

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FILE_NAME, encoding='cp949')
    except:
        df = pd.read_csv(FILE_NAME, encoding='utf-8')
    # 단가 계산 컬럼 추가 ($ / kg)
    df['단가'] = df['당월수출입미화금액(달러)'] / df['당월수출입중량(킬로그램)']
    return df

df = load_data()

# --- 2. 메인 화면 ---
st.title("📊 10월 수산물 수출입 요약 리포트")

# 상단 요약 지표 (10월 전체 데이터 기준)
c1, c2, c3 = st.columns(3)
total_exp = df[df['수출입구분명']=='수출']['당월수출입미화금액(달러)'].sum()
total_imp = df[df['수출입구분명']=='수입']['당월수출입미화금액(달러)'].sum()
c1.metric("10월 총 수출액", f"${total_exp:,.0f}")
c2.metric("10월 총 수입액", f"${total_imp:,.0f}")
c3.metric("무역 수지", f"${total_exp - total_imp:,.0f}")

st.divider()

# --- 3. 시각화 섹션 ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 10월 수출 금액 TOP 10")
    # 수출 데이터 중 상위 10개 추출
    top10_export = df[df['수출입구분명']=='수출'].nlargest(10, '당월수출입미화금액(달러)')
    fig_bar = px.bar(top10_export, x='당월수출입미화금액(달러)', y='수산물수출입품목명', 
                     orientation='h', color='당월수출입미화금액(달러)',
                     title="품목별 수출 순위")
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}) # 높은 순으로 정렬
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("💰 품목별 평균 단가 비교 (Top 10)")
    # 단가가 높은 순으로 상위 10개
    top10_price = df.nlargest(10, '단가')
    fig_scatter = px.scatter(top10_price, x='당월수출입중량(킬로그램)', y='당월수출입미화금액(달러)',
                             size='단가', color='수산물수출입품목명', hover_name='수산물수출입품목명',
                             title="중량 대비 금액 (원의 크기가 단가)")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- 4. 상세 검색 ---
st.subheader("🔍 품목별 상세 정보 검색")
target_item = st.selectbox("품목을 선택하세요", df['수산물수출입품목명'].unique())
item_data = df[df['수산물수출입품목명'] == target_item]
st.table(item_data[['수출입구분명', '당월수출입중량(킬로그램)', '당월수출입미화금액(달러)', '단가']])