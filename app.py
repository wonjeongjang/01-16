import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

# --- [여기서부터 한글 설정 시작] ---
# 윈도우의 '맑은 고딕' 폰트를 설정합니다.
plt.rcParams['font.family'] = 'Malgun Gothic'
# 그래프에서 마이너스(-) 기호가 깨지는 것을 방지합니다.
plt.rcParams['axes.unicode_minus'] = False
# --- [여기까지 한글 설정 끝] ---

st.title("📊 국세청 근로소득 데이터 분석기")

# 데이터 파일 경로
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # 1. 데이터 불러오기 (인코딩 추가)
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("✅ 데이터가 성공적으로 불러와졌습니다!")
    
    # 2. 데이터 미리보기
    st.subheader("📉 데이터 확인하기")
    st.dataframe(df.head(10))

    # 3. 데이터 분석 그래프 그리기
    st.subheader("📈 항목별 분포 그래프")

    # 숫자형 데이터 열만 선택할 수 있게 필터링
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_cols)

        # 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col], ax=ax, color="#cc00ff", kde=True)
        
        # 제목 및 축 레이블 설정 (한글이 적용됨)
        ax.set_title(f"{selected_col} 분포 확인", fontsize=15)
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel("빈도수", fontsize=12)

        # 스트림릿 웹 화면에 그래프 표시
        st.pyplot(fig)
    else:
        st.warning("분석할 수 있는 숫자 데이터가 포함되어 있지 않습니다.")

except FileNotFoundError:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다. 파일 이름을 확인해주세요.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")