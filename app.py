import streamlit as st
from streamlit_option_menu import option_menu
from app.auth.google_auth import google_login
from app.components.profile_management import show_profile_management
from app.components.job_management import show_job_management
import os

# 이미지 URL 설정 (여기에 구글 드라이브 공유 링크를 넣어주세요)
LOGO_URL = "https://drive.google.com/uc?export=view&id=1Pb6HmbxvkXExgTGE7Ygfmqm7PjpxdoR9"

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

def main():
    # CSS 스타일 적용
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
        }
        /* 로그인 전 화면 스타일 */
        .block-container {
            padding: 2rem !important;
            max-width: 100% !important;
        }
        .main-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        .text-container {
            text-align: left;
            color: white;
        }
        [data-testid="stImage"] {
            width: 600px !important;
            margin: 0 auto !important;
            padding: 10rem 2rem 0 2rem !important;
        }
        [data-testid="stImage"] > img {
            margin: 0 !important;
        }
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {
            background-color: #4285f4;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #4285f4;
        }
        /* 로그인 후 메인 영역 스타일 */
        .stApp.authenticated {
            background-color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.get('authenticated'):
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #4285f4;
            }
            </style>
            <div style="text-align: center; padding: 10rem 2rem 0 2rem;">
                <img src="https://i.imgur.com/YOUR_IMGUR_ID.png" width="300"/>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Google 로그인 처리
        google_login()
        return

    # 로그인 후 메인 화면
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://i.imgur.com/YOUR_IMGUR_ID.png" width="150"/>
            </div>
            """,
            unsafe_allow_html=True
        )
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

if __name__ == "__main__":
    main()
