from firebase_admin import auth
import streamlit as st

def verify_token(id_token):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded['uid']
    except Exception as e:
        st.error(f"Invalid token: {e}")
        return None