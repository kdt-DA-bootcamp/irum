import streamlit as st

def show_profile_management():
    st.title("이력 관리")
    
    tabs = st.tabs([
        "기본 인적사항", "학력사항", "경력사항", "기술", 
        "수상경력", "자격증", "대외활동", "병역사항"
    ])
    
    with tabs[0]:
        st.subheader("기본 인적사항")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름")
            birth_date = st.date_input("생년월일")
            phone = st.text_input("연락처")
        with col2:
            email = st.text_input("이메일")
            address = st.text_area("주소")

    with tabs[1]:
        st.subheader("학력사항")
        school = st.text_input("학교명")
        major = st.text_input("전공")
        col1, col2 = st.columns(2)
        with col1:
            admission_year = st.date_input("입학연도")
        with col2:
            graduation_year = st.date_input("졸업연도")
        degree = st.selectbox("학위", ["학사", "석사", "박사", "기타"])

    with tabs[2]:
        st.subheader("경력사항")
        company = st.text_input("회사명")
        position = st.text_input("직무")
        col1, col2 = st.columns(2)
        with col1:
            work_start_date = st.date_input("근무 시작일")
        with col2:
            work_end_date = st.date_input("근무 종료일")
        main_tasks = st.text_area("주요 업무")
        achievements = st.text_area("성과")

    with tabs[3]:
        st.subheader("기술")
        skills = st.text_area("기술명 리스트 (쉼표로 구분)")

    with tabs[4]:
        st.subheader("수상경력")
        award_name = st.text_input("수상명")
        institution = st.text_input("기관")
        award_date = st.date_input("수상일")

    with tabs[5]:
        st.subheader("자격증")
        cert_name = st.text_input("자격증명")
        cert_organization = st.text_input("발급기관")
        cert_date = st.date_input("발급일")

    with tabs[6]:
        st.subheader("대외활동")
        activity_name = st.text_input("활동명")
        organization = st.text_input("소속기관")
        col1, col2 = st.columns(2)
        with col1:
            activity_start_date = st.date_input("활동 시작일")
        with col2:
            activity_end_date = st.date_input("활동 종료일")
        activity_description = st.text_area("활동 내용")

    with tabs[7]:
        st.subheader("병역사항")
        military_service = st.selectbox("복무 여부", ["미해당", "복무완료", "복무중", "면제"])
        if military_service in ["복무완료", "복무중"]:
            col1, col2 = st.columns(2)
            with col1:
                service_start_date = st.date_input("복무 시작일")
            with col2:
                service_end_date = st.date_input("복무 종료일")
            military_branch = st.text_input("병과") 