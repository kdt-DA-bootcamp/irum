import streamlit as st
import requests
from urllib.parse import urlencode

st.set_page_config(page_title="Google OAuth Test")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# OAuth configuration
client_id = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_ID"]
client_secret = st.secrets["google_oauth"]["GOOGLE_OAUTH_CLIENT_SECRET"]
redirect_uri = "https://dreamirum.streamlit.app"

def get_google_auth_url():
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return auth_url

def exchange_code_for_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    response = requests.post(token_url, data=data)
    return response.json() if response.ok else None

def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_info_url, headers=headers)
    return response.json() if response.ok else None

# Handle OAuth callback
if "code" in st.query_params and not st.session_state["authenticated"]:
    code = st.query_params["code"]
    token_data = exchange_code_for_token(code)
    if token_data and "access_token" in token_data:
        user_info = get_user_info(token_data["access_token"])
        if user_info and "email" in user_info:
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = user_info["email"]
            st.rerun()

# Main app
if not st.session_state["authenticated"]:
    st.write("Not logged in")
    auth_url = get_google_auth_url()
    st.markdown(
        f"""
        <a href="{auth_url}" target="_self">
            <button style="background-color: #4285f4; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
                Login with Google
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
else:
    st.write(f"Welcome {st.session_state['user_email']}")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = None
        st.rerun() 