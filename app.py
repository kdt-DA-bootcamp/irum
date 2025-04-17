import streamlit as st

st.set_page_config(page_title="Google OAuth Test")

if not st.experimental_user.is_authenticated:
    st.write("Not logged in")
    st.markdown(
        """
        <a href="/_stcore/authorize" target="_self">
            <button style="background-color: #4285f4; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
                Login with Google
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
else:
    st.write(f"Welcome {st.experimental_user.email}")
    if st.button("Logout"):
        st.experimental_user.logout() 