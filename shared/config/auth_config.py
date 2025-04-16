import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OAuth 2.0 설정
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email'
]

# Google OAuth Redirect URI
GOOGLE_OAUTH_REDIRECT_URI = os.getenv('GOOGLE_OAUTH_REDIRECT_URI') 