import streamlit as st
import random
import datetime # 시간을 다루는 도구 불러오기

st.title("🎰 로또 번호 생성기")
st.header("행운의 로또 번호를 생성해보세요!")

# 로또 번호 생성 함수
def generate_lotto_numbers():
    return sorted(random.sample(range(1, 46), 6))

# 버튼 클릭 시 로또 번호 생성
if st.button("로또 번호 생성"):
    lotto_numbers = generate_lotto_numbers()
    st.success(f"✨ 행운의 로또 번호: {', '.join(map(str, lotto_numbers))}")

# 현재 시각 표시 (import datetime이 있어야 작동함)
st.write(f"생성된 시각 : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")