import streamlit as st

def show_job_management():
    st.title("공고 관리")
    
    # 필수 항목
    st.subheader("필수 항목")
    job_title = st.text_input("공고명")
    company_name = st.text_input("회사명")
    company_website = st.text_input("회사 웹사이트")
    main_duties = st.text_area("주요 업무")
    requirements = st.text_area("자격 요건")
    
    # 선택 항목
    st.subheader("선택 항목")
    preferences = st.text_area("우대 사항")
    ideal_candidate = st.text_area("인재상")
    company_culture = st.text_area("사내 문화") 