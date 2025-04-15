import streamlit as st
from streamlit_option_menu import option_menu
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OAuth 2.0 설정
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# 페이지 기본 설정
st.set_page_config(
    page_title="이룸 - 미래로의 문을 여는 곳",
    page_icon="🚀",
    layout="wide"
)

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

def google_login():
    try:
        # 이미 인증된 경우 처리
        if st.session_state.get('authenticated'):
            return True

        # URL 파라미터에서 인증 코드 확인
        query_params = st.query_params
        if 'code' in query_params:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=SCOPES,
                redirect_uri=os.getenv('GOOGLE_OAUTH_REDIRECT_URI')
            )
            
            code = query_params['code']
            flow.fetch_token(code=code)
            
            # 사용자 인증 완료
            credentials = flow.credentials
            st.session_state['authenticated'] = True
            st.session_state['user_info'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            # 인증 코드 제거를 위한 리디렉션
            st.query_params.clear()
            st.rerun()
            return True
            
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=SCOPES,
                redirect_uri=os.getenv('GOOGLE_OAUTH_REDIRECT_URI')
            )
            
            # 인증 URL 생성
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # 사용자를 인증 페이지로 리다이렉트
            st.markdown(
                f'<div class="login-button"><a href="{authorization_url}" target="_self"><button style="background-color: white; color: #444; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; display: flex; align-items: center; font-size: 16px; font-weight: 500;"><img src="https://www.google.com/favicon.ico" style="margin-right: 10px; width: 18px; height: 18px;">Google 계정으로 계속하기</button></a></div>',
                unsafe_allow_html=True
            )
            return False
            
    except Exception as e:
        st.error(f"로그인 중 오류가 발생했습니다: {str(e)}")
        return False

def main():
    # 페이지 전체 배경색 설정
    st.markdown(
        """
        <style>
        .stApp {
            background-color: """ + ("#4285f4" if not st.session_state.get('authenticated') else "#ffffff") + """;
        }
        .main-content {
            display: flex;
            flex-direction: column;
            color: """ + ("white" if not st.session_state.get('authenticated') else "#000000") + """;
            padding: 2rem;
            max-width: 600px;
            margin: 0 auto;
        }
        .title {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            font-weight: 500;
            text-align: left;
            word-break: keep-all;
            line-height: 1.35;
            width: 100%;
        }
        .subtitle {
            font-size: 1.1rem;
            margin-bottom: 3rem;
            line-height: 1.6;
            text-align: left;
            word-break: keep-all;
            white-space: normal;
            width: 100%;
        }
        .login-section {
            display: flex;
            width: 100%;
            justify-content: flex-start;
            margin-top: 2rem;
        }
        .google-btn {
            background-color: white !important;
            color: #444 !important;
            padding: 12px 24px !important;
            font-size: 16px !important;
            border-radius: 5px !important;
            border: none !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            font-weight: 500 !important;
            text-decoration: none !important;
        }
        .google-btn img {
            margin-right: 10px;
            width: 18px;
            height: 18px;
        }
        /* Center align image */
        div[data-testid="stImage"] {
            display: flex !important;
            justify-content: flex-start !important;
            margin-bottom: 2rem;
            padding-left: 2rem;
        }
        div[data-testid="stImage"] img {
            max-width: 300px !important;
        }
        /* Center column content */
        div[data-testid="column"] {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 100%;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #4285f4;
            color: white;
        }
        section[data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
        section[data-testid="stSidebar"] div[data-testid="stImage"] {
            padding: 1rem;
            margin-bottom: 0;
        }
        /* Option menu styling */
        .nav-link {
            background-color: #4285f4 !important;
            color: white !important;
        }
        .nav-link.active {
            background-color: #3367d6 !important;
            color: white !important;
        }
        .nav-link:hover {
            background-color: #3367d6 !important;
            color: white !important;
        }
        /* Menu container styling */
        nav.nav.nav-pills {
            background-color: #4285f4 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.get('authenticated'):
        # 중앙 정렬을 위한 컬럼 사용
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # 로고 이미지 표시
            st.image("app/assets/logo.png", width=300)
            
            # 인증 URL 생성
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes=SCOPES,
                redirect_uri=os.getenv('GOOGLE_OAUTH_REDIRECT_URI')
            )
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            st.markdown(
                f"""
                <div class="main-content">
                    <div class="title">미래로의 문을 여는 곳, 이룸</div>
                    <div class="subtitle">
                        이룸은 이력 관리와 지원 공고 분석을 통해 취업과 이직을 위한 맞춤형 서류 제작은 물론 경력 관리까지 지원하는 서비스입니다.
                        <br><br>
                        여러분의 경험을 이해하고, 커리어 시장에서 원하는 미래로 나아가는 길을 함께 엽니다.
                    </div>
                    <div class="login-section">
                        <a href="{authorization_url}" target="_self" class="google-btn">
                            <img src="https://www.google.com/favicon.ico" alt="Google logo"/>
                            Google 계정으로 계속하기
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # URL 파라미터에서 인증 코드 확인
            query_params = st.query_params
            if 'code' in query_params:
                code = query_params['code']
                flow.fetch_token(code=code)
                
                # 사용자 인증 완료
                credentials = flow.credentials
                st.session_state['authenticated'] = True
                st.session_state['user_info'] = {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }
                
                # 인증 코드 제거를 위한 리디렉션
                st.query_params.clear()
                st.rerun()
            return

    # 로그인 후 메인 화면
    with st.sidebar:
        st.image("app/assets/logo.png", width=150)
        selected = option_menu(
            menu_title=None,
            options=["대시보드", "이력 관리", "공고 관리", "서류 관리"],
            icons=["house", "person-vcard", "briefcase", "file-earmark-text"],
            menu_icon="house",
            default_index=0,
            styles={
                "container": {"background-color": "#4285f4"},
                "icon": {"color": "white"},
                "nav-link": {"color": "white"},
                "nav-link-selected": {"background-color": "#3367d6"},
                "menu-title": {"color": "white"},
                "menu-icon": {"color": "white"}
            }
        )

    # 메인 컨텐츠
    if selected == "대시보드":
        st.title("대시보드")
        st.write("대시보드 기능은 준비 중입니다.")
    elif selected == "이력 관리":
        show_profile_management()
    elif selected == "공고 관리":
        show_job_management()
    elif selected == "서류 관리":
        st.title("서류 관리")
        st.write("서류 관리 기능은 준비 중입니다.")

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

if __name__ == "__main__":
    main()
