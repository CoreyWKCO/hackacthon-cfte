import streamlit as st
from utils.auth import get_current_user, logout

def render():
    st.title("⚙️ Settings")
    st.info("Configure your preferences")
    
    current_user = get_current_user()
    if not current_user:
        st.warning("Please login to access this feature")
        return
    
    st.subheader("User Preferences")
    st.text_input("Display Name", value=current_user.get('username', current_user.get('email', 'User')))
    st.selectbox("Theme", ["Light", "Dark", "Auto"])
    st.slider("Font Size", 12, 24, 16)
    
    if st.button("Save Preferences"):
        st.success("Preferences saved!")
    
    st.markdown("---")
    st.subheader("Account")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Change Password", use_container_width=True):
            st.info("Password change feature coming soon!")
    with col2:
        if st.button("Delete Account", use_container_width=True, type="secondary"):
            st.warning("Account deletion feature coming soon!")