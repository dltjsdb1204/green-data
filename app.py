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

elif menu == "자가진단 (상태 체크)":
    st.header("🔍 전문 심리 척도 자가진단")
    st.write("병원 및 상담 센터에서 실제 사용하는 검증된 문항입니다. 현재 상태를 솔직하게 체크해 주세요.")

    # 탭을 나누어 여러 검사를 제공
    tab1, tab2, tab3 = st.tabs(["우울증 (GDS-K)", "스트레스 (PSS)", "불면 및 번아웃"])

    # --- 탭 1: 노인우울척도 (GDS-K) 단축판 ---
    with tab1:
        st.subheader("단축형 노인우울척도 (GDS-K)")
        st.caption("지난 일주일 동안 느끼신 감정을 '예/아니오'로 선택해 주세요.")
        
        gds_questions = [
            "1. 현재의 생활에 대체로 만족하십니까?",
            "2. 활동이나 관심거리가 많이 줄었습니까?",
            "3. 삶이 비어 있는 것 같이 느끼십니까?",
            "4. 종종 마음이 지루하고 따분하십니까?",
            "5. 앞날에 대해 희망적이십니까?",
            "6. 떨쳐버릴 수 없는 생각들 때문에 괴로우십니까?",
            "7. 대체로 활기차게 사시는 편입니까?",
            "8. 자신에게 불행한 일이 일어날 것 같아 걱정하십니까?"
        ]
        
        gds_score = 0
        for i, q in enumerate(gds_questions):
            ans = st.radio(q, ["예", "아니오"], key=f"gds_{i}")
            # 역채점 문항(1, 5, 7번) 처리 로직
            if i in [0, 4, 6]:
                if ans == "아니오": gds_score += 1
            else:
                if ans == "예": gds_score += 1

        if st.button("우울증 결과 확인"):
            st.info(f"당신의 GDS-K 점수는 **{gds_score}점**입니다.")
            if gds_score >= 5:
                st.warning("주의: 가벼운 우울감이 의심됩니다. 치유농업 프로그램을 통한 정서적 환기를 추천합니다.")
            else:
                st.success("정상: 현재 심리적으로 안정된 상태입니다.")

    # --- 탭 2: 지각된 스트레스 척도 (PSS) ---
    with tab2:
        st.subheader("지각된 스트레스 척도 (PSS-10)")
        st.caption("지난 한 달 동안 얼마나 자주 느끼셨는지 선택해 주세요.")
        
        pss_options = {0: "전혀 없었다", 1: "거의 없었다", 2: "가끔 있었다", 3: "꽤 자주 있었다", 4: "매우 자주 있었다"}
        
        pss_questions = [
            "1. 예상치 못한 일 때문에 당황한 적이 얼마나 있었습니까?",
            "2. 인생에서 중요한 일들을 통제할 수 없다고 느낀 적이 얼마나 있었습니까?",
            "3. 신경이 예민해지고 스트레스를 받는다고 느낀 적이 얼마나 있었습니까?",
            "4. 개인적인 문제를 처리하는 능력에 자신감을 느낀 적이 얼마나 있었습니까? (역채점)"
        ]
        
        pss_score = 0
        for i, q in enumerate(pss_questions):
            val = st.select_slider(q, options=[0, 1, 2, 3, 4], format_func=lambda x: pss_options[x], key=f"pss_{i}")
            if i == 3: # 4번 문항 역채점
                pss_score += (4 - val)
            else:
                pss_score += val

        if st.button("스트레스 결과 확인"):
            st.write(f"당신의 스트레스 점수는 **{pss_score}점**입니다. (4문항 기준)")
            if pss_score >= 8:
                st.error("고위험: 현재 심한 스트레스 상태입니다. 전문적인 상담 혹은 숲 치유 프로그램이 시급합니다.")
            else:
                st.success("양호: 스트레스를 잘 관리하고 계십니다.")

    # --- 탭 3: 불면 및 번아웃 ---
    with tab3:
        st.subheader("불면증 및 번아웃 간이 체크")
        insomnia = st.checkbox("잠들기 어렵거나 자다가 자주 깹니다.")
        burnout = st.checkbox("업무/학업 후 진이 다 빠져서 아무것도 할 수 없습니다.")
        
        if st.button("종합 소견 보기"):
            if insomnia and burnout:
                st.warning("불면과 번아웃이 동시에 나타나고 있습니다. '휴식형 치유농장' 매칭을 권장합니다.")
            else:
                st.write("체크하신 항목을 바탕으로 맞춤형 농가를 필터링합니다.")

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
