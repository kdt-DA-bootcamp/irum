import streamlit as st
from datetime import datetime
from typing import List
import json
from app.schemas.resume import ResumeData, Education, WorkExperience, Award, Certification, Activity, MilitaryService
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.resume import UserResume, ParseStatus

st.set_page_config(page_title="이력서 입력 시스템", layout="wide")

def init_session_state():
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'personal_info': {},
            'education': [],
            'work_experience': [],
            'skills': [],
            'awards': [],
            'certifications': [],
            'activities': [],
            'military_service': {}
        }

def input_personal_info():
    st.subheader("기본 인적사항")
    with st.form("personal_info_form"):
        name = st.text_input("이름")
        birth_date = st.date_input("생년월일")
        phone = st.text_input("연락처")
        email = st.text_input("이메일")
        address = st.text_input("주소")
        
        if st.form_submit_button("저장"):
            st.session_state.resume_data['personal_info'] = {
                'name': name,
                'birth_date': birth_date.isoformat(),
                'phone': phone,
                'email': email,
                'address': address
            }
            st.success("기본 인적사항이 저장되었습니다.")

def input_education():
    st.subheader("학력사항")
    with st.form("education_form"):
        school_name = st.text_input("학교명")
        major = st.text_input("전공")
        start_date = st.date_input("입학일")
        end_date = st.date_input("졸업일")
        degree = st.text_input("학위")
        
        if st.form_submit_button("추가"):
            education = {
                'school_name': school_name,
                'major': major,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'degree': degree
            }
            st.session_state.resume_data['education'].append(education)
            st.success("학력사항이 추가되었습니다.")

def input_work_experience():
    st.subheader("경력사항")
    with st.form("work_experience_form"):
        company_name = st.text_input("회사명")
        position = st.text_input("직무")
        start_date = st.date_input("입사일")
        end_date = st.date_input("퇴사일")
        main_duties = st.text_area("주요 업무 (줄바꿈으로 구분)").split('\n')
        achievements = st.text_area("성과 (줄바꿈으로 구분)").split('\n')
        
        if st.form_submit_button("추가"):
            work_exp = {
                'company_name': company_name,
                'position': position,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'main_duties': main_duties,
                'achievements': achievements
            }
            st.session_state.resume_data['work_experience'].append(work_exp)
            st.success("경력사항이 추가되었습니다.")

def input_skills():
    st.subheader("기술")
    skills = st.text_area("기술 (쉼표로 구분)")
    if st.button("기술 저장"):
        st.session_state.resume_data['skills'] = [s.strip() for s in skills.split(',')]
        st.success("기술이 저장되었습니다.")

def save_resume():
    if st.button("이력서 저장"):
        try:
            db = next(get_db())
            resume = UserResume(
                user_id=1,  # TODO: 실제 사용자 ID로 변경
                resume_data=st.session_state.resume_data,
                parsed_status=ParseStatus.SUCCESS
            )
            db.add(resume)
            db.commit()
            st.success("이력서가 성공적으로 저장되었습니다.")
        except Exception as e:
            st.error(f"이력서 저장 중 오류가 발생했습니다: {str(e)}")

def main():
    st.title("이력서 입력 시스템")
    
    init_session_state()
    
    input_personal_info()
    input_education()
    input_work_experience()
    input_skills()
    
    save_resume()
    
    # 저장된 데이터 미리보기
    if st.checkbox("저장된 데이터 미리보기"):
        st.json(st.session_state.resume_data)

if __name__ == "__main__":
    main()