import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

# 한글 폰트 설정 (그래프 내부 한글 깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("📊 국세청 근로소득 데이터 분석기")

file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # 인코딩 옵션 추가: 한국 공공기관 데이터는 주로 'cp949'를 사용합니다.
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("✅ 데이터가 성공적으로 불러와졌습니다!")
    
    st.subheader("📉 데이터 확인하기")
    st.dataframe(df.head(10))

    st.subheader("📈 항목별 분포 그래프")

    # 숫자형 데이터 열만 추출
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_cols)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col], ax=ax, color="#cc00ff", kde=True)
        ax.set_title(f"{selected_col} 분포 확인")
        ax.set_xlabel(selected_col)
        ax.set_ylabel("빈도수")

        st.pyplot(fig)
    else:
        st.warning("데이터셋에 분석 가능한 숫자형 항목이 없습니다.")

except FileNotFoundError:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다.")
except UnicodeDecodeError:
    st.error("❌ 파일 인코딩 오류가 발생했습니다. 'utf-8'이나 'cp949' 형식을 확인해 주세요.")
except Exception as e:
    st.error(f"❌ 오류가 발생했습니다: {e}")
    