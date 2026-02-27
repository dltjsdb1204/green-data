import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 기억장치(session_state) 세팅
st.set_page_config(page_title="그린데이터", layout="wide")

# [핵심] 사용자의 진단 결과를 기억할 공간을 만듭니다. 처음에 들어오면 '미진단' 상태입니다.
if 'user_condition' not in st.session_state:
    st.session_state.user_condition = "미진단"

# 2. 사이드바 메뉴
st.sidebar.title("🌱 그린데이터 메뉴")
menu = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["홈 (서비스 소개)", "자가진단 (상태 체크)", "치유농가 소개 (매칭)", "나의 치유 리포트 (데이터 열람)"]
)

# --- 탭 1: 홈 (서비스 소개) ---
if menu == "홈 (서비스 소개)":
    st.header("농업이 치료가 되다, 그린데이터")
    st.markdown("### 대한민국은 OECD 국가 중 우울증 유병률 1위입니다.")
    st.write("그린데이터는 고령화로 인한 노인 고립 문제와 2030 세대의 번아웃을 치유농업으로 해결하고자 합니다.")

# --- 탭 2: 자가진단 (상태 체크) ---
elif menu == "자가진단 (상태 체크)":
    st.header("🔍 전문 분야별 자가진단")
    st.write("병원 및 심리상담센터에서 실제 사용하는 공신력 있는 문항입니다. 답변을 제출하면 맞춤 농가가 세팅됩니다.")

    diagnosis_type = st.tabs(["우울증 진단 (BDI)", "치매 선별 (S-SDQ)", "번아웃 증후군"])

    # 1) 우울증 진단
    with diagnosis_type[0]:
        st.subheader("우울증 진단 (Beck Depression Inventory)")
        
        bdi_questions = [
            ["나는 슬프지 않다.", "나는 슬프다.", "나는 가끔 슬플 때가 있다.", "나는 항상 슬퍼서 그것을 떨쳐버릴 수가 없다."],
            ["나는 앞날에 대해 별로 낙심하지 않는다.", "나는 앞날에 대해 비관적인 느낌이 든다.", "나는 앞날에 대해 기대할 것이 아무 것도 없다고 느낀다.", "나의 앞날은 아주 절망적이고 나아질 가능성이 없다고 느낀다."],
            ["나는 실패자라고 느끼지 않는다.", "나는 보통사람들보다 더 많이 실패한 것 같다.", "내가 살아온 과거를 되돌아보면, 생각나는 것은 실패 뿐이다.", "나는 인간으로서 완전한 실패자인 것 같다."],
            ["나는 전과 같이 일상생활에 만족하고 있다.", "나의 일상생활은 전처럼 즐겁지 않다.", "나는 더 이상 어떤 것에서도 참된 만족을 얻지 못한다.", "나는 모든 것이 다 불만스럽고 지겹다."],
            ["나는 특별히 죄책감을 느끼지 않는다.", "나는 죄책감을 느낄 때가 많다.", "나는 거의 언제나 죄책감을 느낀다.", "나는 항상 언제나 죄책감을 느낀다."]
            # (테스트를 위해 5번까지만 넣었습니다. 언제든 이전 코드의 21번까지 복사해 넣으셔도 똑같이 작동합니다!)
        ]
        
        with st.form("bdi_form"):
            bdi_answers = []
            for i, options in enumerate(bdi_questions):
                choice = st.radio(f"{i+1}번 문항", options, key=f"bdi_{i}")
                bdi_answers.append(choice)
            bdi_submitted = st.form_submit_button("우울증 결과 분석")
            
        if bdi_submitted:
            bdi_score = sum([options.index(ans) for options, ans in zip(bdi_questions, bdi_answers)])
            st.info(f"📊 BDI 총점: {bdi_score}점")
            
            if bdi_score >= 10: # (5문항 기준 임시 컷오프)
                st.error("주의: 우울감이 높은 상태입니다. '치유농가 소개' 탭에서 추천 농장을 확인하세요.")
                # [상태 저장] 우울/스트레스 상태로 기억합니다!
                st.session_state.user_condition = "우울/스트레스" 
            else:
                st.success("양호: 우울감이 정상 범위입니다. '치유농가 소개' 탭에서 추천 농장을 확인하세요.")
                # [상태 저장] 정상 범위이므로 예방/휴식 상태로 기억합니다!
                st.session_state.user_condition = "예방/휴식"

    # 2) 치매 선별 진단
    with diagnosis_type[1]:
        st.subheader("단축형 삼성 치매 선별 질문지 (S-SDQ)")
        
        ssdq_questions = [
            "1. 언제 어떤 일이 일어났는지 기억하지 못한다.",
            "2. 며칠 전에 들었던 이야기를 잊는다.",
            "3. 반복되는 일상생활에 변화가 생겼을 때 금방 적응하기가 힘들다.",
            "4. 본인에게 중요한 사항을 잊는다.",
            "5. 어떤 일을 해놓고 잊어버려 다시 반복 한다."
        ]
        ssdq_options = {"그렇지 않다": 0, "간혹(약간) 그렇다": 1, "자주(많이) 그렇다": 2}
        
        with st.form("ssdq_form"):
            ssdq_answers = []
            for i, q in enumerate(ssdq_questions):
                choice = st.select_slider(q, options=list(ssdq_options.keys()), key=f"ssdq_{i}")
                ssdq_answers.append(choice)
            ssdq_submitted = st.form_submit_button("치매 선별 결과 확인")
            
        if ssdq_submitted:
            ssdq_score = sum([ssdq_options[ans] for ans in ssdq_answers])
            st.info(f"📊 S-SDQ 총점: {ssdq_score}점")
            
            if ssdq_score >= 8:
                st.error("치매 의심: 총점이 8점 이상입니다. '치유농가 소개' 탭에서 인지 특화 농장을 확인하세요.")
                # [상태 저장] 치매 위험군으로 기억합니다!
                st.session_state.user_condition = "치매 위험군"
            else:
                st.success("양호: 정상 범위 내에 있습니다.")
                st.session_state.user_condition = "예방/휴식"

    # 3) 번아웃 진단
    with diagnosis_type[2]:
        st.subheader("마음소풍 번아웃 증후군 자가진단")
        
        burnout_questions = [
            "1. 출근하는 생각만 해도 짜증과 함께 가슴이 답답함을 느낀다.",
            "2. 직장에서 칭찬을 들어도 썩 즐거운 기분이 들지 않는다.",
            "3. 직장생활 외에 개인적인 생활이나 시간이 거의 없다."
        ]
        bo_options = {"아니다": 0, "가끔 그렇다": 1, "자주 그렇다": 2}
        
        with st.form("bo_form"):
            bo_answers = []
            for i, q in enumerate(burnout_questions):
                choice = st.radio(q, list(bo_options.keys()), key=f"bo_{i}", horizontal=True)
                bo_answers.append(choice)
            bo_submitted = st.form_submit_button("번아웃 지수 확인")
            
        if bo_submitted:
            bo_score = sum([bo_options[ans] for ans in bo_answers])
            st.info(f"📊 번아웃 점수: {bo_score}점")
            
            if bo_score >= 4:
                st.warning("번아웃 경고: 휴식이 필요합니다. '치유농가 소개' 탭에서 힐링 농장을 확인하세요.")
                # [상태 저장] 번아웃 상태로 기억합니다!
                st.session_state.user_condition = "번아웃"
            else:
                st.success("양호: 에너지를 잘 관리하고 계십니다.")
                st.session_state.user_condition = "예방/휴식"

# --- 탭 3: 치유농가 소개 (매칭) ---
elif menu == "치유농가 소개 (매칭)":
    st.header("🏡 맞춤형 치유농장 큐레이션")
    
    # 가상의 농가 데이터베이스 
    farms_data = pd.DataFrame([
        {"농장명": "초록 쉼터 (서울)", "프로그램": "허브 재배 및 명상", "추천 대상": "우울/스트레스", "전문성": "치유농업사 1급 상주"},
        {"농장명": "기억 쑥쑥 농장 (경기)", "프로그램": "과일 수확 및 인지 훈련", "추천 대상": "치매 위험군", "전문성": "장기요양 인지활동형 충족"},
        {"농장명": "마음 챙김 포레스트 (강원)", "프로그램": "동물 교감 및 불멍", "추천 대상": "번아웃", "전문성": "EAP(근로자지원) 제휴"},
        {"농장명": "패밀리 팜 (경기)", "프로그램": "주말 텃밭 가꾸기", "추천 대상": "예방/휴식", "전문성": "일반 체험 중심"},
        {"농장명": "햇살 가득 농원 (충청)", "프로그램": "꽃꽂이 및 원예 치료", "추천 대상": "우울/스트레스", "전문성": "원예심리상담사 보유"}
    ])

    # [매칭 로직] 기억장치에 저장된 사용자 상태를 불러옵니다.
    current_condition = st.session_state.user_condition

    if current_condition == "미진단":
        st.warning("앗! 아직 자가진단을 하지 않으셨네요. 정확한 매칭을 위해 먼저 상태를 체크해주세요.")
        st.write("아래는 전체 농가 목록입니다.")
        st.dataframe(farms_data)
        
    else:
        st.success(f"현재 고객님의 상태는 **'{current_condition}'** 특화 프로그램이 필요합니다. 맞춤 농가를 찾았습니다!")
        
        # [매칭 로직] 농가 데이터 중 '추천 대상'이 사용자의 상태와 똑같은 곳만 걸러냅니다.
        matched_farms = farms_data[farms_data["추천 대상"] == current_condition]
        
        # 필터링된 농가를 화면에 출력
        for index, row in matched_farms.iterrows():
            with st.container():
                st.markdown(f"### 🌿 {row['농장명']}")
                st.write(f"- **진행 프로그램:** {row['프로그램']}")
                st.write(f"- **전문성:** {row['전문성']}")
                st.markdown("---")

# --- 탭 4: 나의 치유 리포트 (데이터 열람) ---
elif menu == "나의 치유 리포트 (데이터 열람)":
    st.header("📊 데이터 기반 치유 효과 리포트")
    st.write("웨어러블 API 연동을 통한 객관적 수치 확인 페이지입니다. (현재 준비 중)")
