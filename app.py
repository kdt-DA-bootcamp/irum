import streamlit as st
from streamlit_option_menu import option_menu
from app.components.profile_management import show_profile_management
from app.components.job_management import show_job_management
import os
import requests
import json
from urllib.parse import quote_plus

# 이미지 URL 설정
LOGO_URL = "https://i.imgur.com/thQZtYk.png"

# 페이지 기본 설정
st.set_page_config(
    page_title="이룸 - 미래로의 문을 여는 곳",
    page_icon="🚀",
    layout="wide"
)

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

def exchange_code_for_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    client_id = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_ID"]
    client_secret = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_SECRET"]
    redirect_uri = 'https://dreamirum.streamlit.app'
    
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=data)
    if not response.ok:
        st.error("로그인 처리 중 오류가 발생했습니다. 다시 시도해주세요.")
    if response.ok:
        return response.json()
    return None

def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(user_info_url, headers=headers)
    st.write("User Info Response Status:", response.status_code)
    if not response.ok:
        st.write("User Info Error:", response.text)
    if response.ok:
        return response.json()
    return None

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
        [data-testid="stElementContainer"] {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        [data-testid="stFullScreenFrame"] {
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 600px;
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

    # OAuth 콜백 처리
    params = st.query_params
    if 'code' in params and not st.session_state['authenticated']:
        code = params['code']
        st.write("Received authorization code:", code)
        token_data = exchange_code_for_token(code)
        
        if token_data:
            st.write("Token data received:", json.dumps(token_data, indent=2))
            if 'access_token' in token_data:
                user_info = get_user_info(token_data['access_token'])
                if user_info and 'email' in user_info:
                    st.session_state['authenticated'] = True
                    st.session_state['user_email'] = user_info['email']
                    params.clear()
                    st.rerun()
            else:
                st.write("No access token in token data")
        else:
            st.write("Failed to exchange code for token")

    # 로그인 상태 확인
    if not st.session_state['authenticated']:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #4285f4;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # 로고
        st.image(LOGO_URL, width=300)
        
        # 텍스트
        st.markdown(
            """
            <div class="main-container">
                <div class="text-container">
                    <h1 style="font-size: 2rem; margin-bottom: 1.5rem; font-weight: 500; line-height: 1.35; color: white;">미래로의 문을 여는 곳, 이룸</h1>
                    <div style="font-size: 1.1rem; margin-bottom: 3rem; line-height: 1.6; color: white;">
                        이룸은 이력 관리와 지원 공고 분석을 통해 취업과 이직을 위한 맞춤형 서류 제작은 물론 경력 관리까지 지원하는 서비스입니다.
                        <br><br>
                        여러분의 경험을 이해하고, 커리어 시장에서 원하는 미래로 나아가는 길을 함께 엽니다.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # OAuth 로그인 버튼
        client_id = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_ID"]
        redirect_uri = quote_plus('https://dreamirum.streamlit.app')
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            "response_type=code&"
            "scope=openid%20email%20profile&"
            "access_type=online&"
            "include_granted_scopes=true&"
            "prompt=select_account"
        )
        
        st.write("Generated Auth URL:", auth_url)
        
        st.markdown(
            f"""
            <div class="main-container">
                <div class="text-container">
                    <a href="{auth_url}" target="_self" onclick="console.log('Auth URL:', this.href);">
                        <button style="background-color: white; color: #444; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: 500; display: flex; align-items: center;">
                            <img src="https://www.google.com/favicon.ico" style="width: 18px; height: 18px; margin-right: 10px;">
                            Sign in with Google
                        </button>
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # 로그인 후 메인 화면
    with st.sidebar:
        st.image(LOGO_URL, width=150)
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
        st.write(f"환영합니다, {st.session_state['user_email']}님!")
        st.write("대시보드 기능은 준비 중입니다.")
        if st.button("로그아웃"):
            st.session_state['authenticated'] = False
            st.session_state['user_email'] = None
            st.rerun()
    elif selected == "이력 관리":
        show_profile_management()
    elif selected == "공고 관리":
        show_job_management()
    elif selected == "서류 관리":
        st.title("서류 관리")
        st.write("서류 관리 기능은 준비 중입니다.")

if __name__ == "__main__":
    main()
