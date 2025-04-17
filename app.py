import streamlit as st

st.set_page_config(page_title="Google OAuth Test")

if not st.experimental_user.is_authenticated:
    st.button('Login with Google')
else:
    st.write(f'Welcome {st.experimental_user.email}')
    st.button('Logout', on_click=st.experimental_user.logout) 