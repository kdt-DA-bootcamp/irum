import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from shared.config.auth_config import SCOPES
from streamlit_google_auth import Authenticate

def init_google_auth():
    authenticator = Authenticate(
        secret_credentials_path='client_secret.json',
        cookie_name='irum_auth',
        cookie_key='irum_secret_key',
        redirect_uri='https://dreamirum.streamlit.app',
    )
    return authenticator

def google_login():
    authenticator = init_google_auth()
    
    # 인증 상태 확인
    authenticator.check_authentification()
    
    # 로그인 버튼 표시
    authenticator.login()
    
    if st.session_state.get('connected'):
        return {
            'name': st.session_state['user_info'].get('name'),
            'email': st.session_state['user_info'].get('email'),
            'picture': st.session_state['user_info'].get('picture')
        }
    return None

def google_logout():
    authenticator = init_google_auth()
    authenticator.logout()

def google_login_old():
    try:
        # 이미 인증된 경우 처리
        if st.session_state.get('authenticated'):
            return True

        # 환경 변수에서 클라이언트 정보 가져오기
        client_config = {
            "web": {
                "client_id": st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_ID"],
                "client_secret": st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["https://dreamirum.streamlit.app"]
            }
        }

        # OAuth 설정
        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri="https://dreamirum.streamlit.app"
        )

        # URL 파라미터에서 인증 코드 확인
        query_params = st.query_params
        if 'code' in query_params:
            try:
                flow.fetch_token(code=query_params['code'])
                
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
            except Exception as e:
                st.error(f"인증 코드 처리 중 오류가 발생했습니다: {str(e)}")
                return False
            
        else:
            # 인증 URL 생성
            authorization_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            # 사용자를 인증 페이지로 리다이렉트
            st.markdown(
                f"""
                <div class="main-container">
                    <div style="text-align: left;">
                        <a href="{authorization_url}" target="_self">
                            <button style="background-color: white; color: #444; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; display: inline-flex; align-items: center; font-size: 16px; font-weight: 500;">
                                <img src="https://www.google.com/favicon.ico" style="margin-right: 10px; width: 18px; height: 18px;">
                                Google 계정으로 계속하기
                            </button>
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            return False
            
    except Exception as e:
        st.error(f"로그인 중 오류가 발생했습니다: {str(e)}")
        return False 