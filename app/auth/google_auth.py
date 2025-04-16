import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from shared.config.auth_config import SCOPES, GOOGLE_OAUTH_REDIRECT_URI

def google_login():
    try:
        # 이미 인증된 경우 처리
        if st.session_state.get('authenticated'):
            return True

        # 환경 변수에서 클라이언트 정보 가져오기
        client_id = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_ID"]
        client_secret = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_SECRET"]
        
        if not client_id or not client_secret:
            st.error("Google OAuth 설정이 필요합니다.")
            return

        # OAuth 설정
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [GOOGLE_OAUTH_REDIRECT_URI],
                }
            },
            scopes=SCOPES
        )
        
        # URL 파라미터에서 인증 코드 확인
        query_params = st.query_params
        if 'code' in query_params and 'state' in query_params:
            try:
                flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI
                flow.fetch_token(
                    authorization_response=f"{GOOGLE_OAUTH_REDIRECT_URI}?code={query_params['code']}&state={query_params['state']}"
                )
                
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
            flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            # state를 세션에 저장
            st.session_state['oauth_state'] = state
            
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