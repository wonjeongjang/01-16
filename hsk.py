import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="10월 수산물 무역 리포트", layout="wide")

FILE_NAME = '해양수산부_HSK품목별수출입현황_20251031.csv' 

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FILE_NAME, encoding='cp949')
    except:
        df = pd.read_csv(FILE_NAME, encoding='utf-8')
    
    # [보완] 중량이 0이거나 데이터가 없는 경우 제외 (계산 오류 방지)
    df = df[df['당월수출입중량(킬로그램)'] > 0].copy()
    
    # 단가 계산 ($ / kg)
    df['단가'] = df['당월수출입미화금액(달러)'] / df['당월수출입중량(킬로그램)']
    return df

try:
    df = load_data()

    st.title("📊 10월 수산물 수출입 요약 리포트")

    # --- 상단 요약 지표 ---
    c1, c2, c3 = st.columns(3)
    # 가독성을 위해 데이터 추출 시 .get()이나 조건문 활용
    exp_df = df[df['수출입구분명']=='수출']
    imp_df = df[df['수출입구분명']=='수입']
    
    total_exp = exp_df['당월수출입미화금액(달러)'].sum()
    total_imp = imp_df['당월수출입미화금액(달러)'].sum()
    
    c1.metric("10월 총 수출액", f"${total_exp:,.0f}")
    c2.metric("10월 총 수입액", f"${total_imp:,.0f}")
    c3.metric("무역 수지", f"${total_exp - total_imp:,.0f}", delta_color="normal")

    st.divider()

    # --- 시각화 섹션 ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🏆 10월 수출 금액 TOP 10")
        top10_export = exp_df.nlargest(10, '당월수출입미화금액(달러)')
        fig_bar = px.bar(top10_export, x='당월수출입미화금액(달러)', y='수산물수출입품목명', 
                         orientation='h', 
                         color='당월수출입미화금액(달러)',
                         color_continuous_scale='Blues', # 색상 일관성
                         labels={'당월수출입미화금액(달러)':'수출액($)'})
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("💰 품목별 평균 단가 분석 (Top 10)")
        top10_price = df.nlargest(10, '단가')
        fig_scatter = px.scatter(top10_price, x='당월수출입중량(킬로그램)', y='당월수출입미화금액(달러)',
                                 size='단가', color='수산물수출입품목명', 
                                 size_max=60, # 버블 크기 조정
                                 labels={'단가':'단가($/kg)'})
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- 상세 검색 ---
    st.subheader("🔍 품목별 상세 정보 검색")
    target_item = st.selectbox("품목을 선택하세요", sorted(df['수산물수출입품목명'].unique()))
    item_data = df[df['수산물수출입품목명'] == target_item].copy()
    
    # 테이블 출력 전 포맷팅 (소수점 정리)
    item_data['단가'] = item_data['단가'].map('${:,.2f}'.format)
    st.table(item_data[['수출입구분명', '당월수출입중량(킬로그램)', '당월수출입미화금액(달러)', '단가']])

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")