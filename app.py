import streamlit as st

st.set_page_config(page_title="Google OAuth Test")

if not st.experimental_user.is_authenticated:
    st.write("Not logged in")
    st.button("Login with Google")
else:
    st.write(f"Welcome {st.experimental_user.email}")
    if st.button("Logout"):
        st.experimental_user.logout() 