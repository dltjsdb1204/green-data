import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정 [cite: 19]
st.set_page_config(page_title="그린데이터", layout="wide")

# 사이드바 메뉴 (사용자 선택 탭) [cite: 17, 19, 228]
st.sidebar.title("🌱 그린데이터 메뉴")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["홈 (서비스 소개)", "자가진단 (상태 체크)", "치유농가 소개 (매칭)", "나의 치유 리포트 (데이터 열람)"]
)

# --- 탭 1: 홈 (서비스 소개) --- [cite: 5, 18]
if menu == "홈 (서비스 소개)":
    st.header("농업이 치료가 되다, 그린데이터")
    st.markdown("### 대한민국은 OECD 국가 중 우울증 유병률 1위입니다. [cite: 7]")
    st.write("그린데이터는 고령화로 인한 노인 고립 문제와 2030 세대의 번아웃을 치유농업으로 해결하고자 합니다. [cite: 8]")
    st.info("국내 치유농업의 사회경제적 가치는 약 3.7조 원 규모로 전망됩니다. [cite: 81, 82]")

# --- 탭 2: 자가진단 (상태 체크) --- [cite: 24, 45, 46]
elif menu == "자가진단 (상태 체크)":
    st.header("🔍 나의 현재 상태 체크")
    st.write("AI 챗봇이 대화하듯 상태를 체크하여 정확한 농가를 추천해 드립니다. [cite: 46]")
    
    with st.form("diagnosis_form"):
        # 노인우울척도(GDS-K) 및 지각된 스트레스 척도(PSS) 항목 반영 
        q1 = st.selectbox("현재 가장 큰 고민은 무엇인가요? [cite: 24]", ["스트레스", "불면증", "우울감", "기타"])
        q2 = st.slider("최근 일주일간 느끼신 스트레스 정도 (0-10) [cite: 24]", 0, 10, 5)
        location = st.text_input("거주 지역을 입력해주세요 (예: 서울시 강남구) [cite: 24]")
        
        if st.form_submit_button("진단 및 매칭 시작"):
            st.success(f"{location} 주변의 최적합 치유농가를 검색합니다. [cite: 27]")

# --- 탭 3: 치유농가 소개 (매칭) --- [cite: 25, 72, 73]
elif menu == "치유농가 소개 (매칭)":
    st.header("🏡 맞춤형 치유농장 추천")
    st.write("자체 품질 지표(F-QIS)를 통해 엄선된 농장들입니다. [cite: 73, 232]")
    
    # 예시 데이터 (계획서 상의 농가 데이터 기반) [cite: 25, 26, 74, 75]
    farms = [
        {"농장명": "A 치유농장", "프로그램": "식물재배", "전문인력": "치유농업사 보유", "편의시설": "휠체어 접근 가능"},
        {"농장명": "B 치유농장", "프로그램": "동물교감", "전문인력": "의학적 근거 보유", "편의시설": "응급키트 구비"}
    ]
    st.table(pd.DataFrame(farms))

# --- 탭 4: 나의 치유 리포트 (데이터 열람) --- [cite: 17, 30, 31]
elif menu == "나의 치유 리포트 (데이터 열람)":
    st.header("📊 데이터 기반 치유 효과 리포트")
    st.write("웨어러블 API 연동을 통한 객관적 수치 확인이 가능합니다. [cite: 30, 189]")
    
    # 스트레스 저항도(SDNN) 변화 시각화 예시 [cite: 44, 197]
    report_data = pd.DataFrame({
        "측정 시점": ["프로그램 전", "프로그램 후"],
        "스트레스 저항도 점수": [45, 78] 
    })
    fig = px.line(report_data, x="측정 시점", y="스트레스 저항도 점수", markers=True, title="치유 프로그램 참여 후 효과 검증")
    st.plotly_chart(fig)
