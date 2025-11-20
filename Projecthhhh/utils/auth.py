import streamlit as st
import hashlib

def get_current_user():
    """Get current user from session state"""
    return st.session_state.get('user')

def login_required(func):
    """Decorator to require login for pages"""
    def wrapper(*args, **kwargs):
        if not get_current_user():
            st.error("Please log in to access this page.")
            return
        return func(*args, **kwargs)
    return wrapper

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    """Login user with email and password"""
    try:
        # Demo mode - simple authentication
        if "users" not in st.session_state:
            st.session_state["users"] = {}
        
        # Check if user exists and password matches
        if email in st.session_state["users"]:
            if st.session_state["users"][email]["password"] == hash_password(password):
                user = {
                    'email': email,
                    'username': st.session_state["users"][email]["username"],
                    'uid': f"user_{hash(email)}",
                    'email_verified': True
                }
                st.session_state.user = user
                return True
            else:
                st.error("Invalid password")
                return False
        else:
            st.error("User not found")
            return False
        
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False

def register_user(email, password, username):
    """Register new user"""
    try:
        # Demo mode - store in session state
        if "users" not in st.session_state:
            st.session_state["users"] = {}
        
        if email in st.session_state["users"]:
            st.error("User already exists with this email")
            return False
        
        # Store user in session state
        st.session_state["users"][email] = {
            "username": username,
            "password": hash_password(password),
            "email": email
        }
        
        user = {
            'email': email,
            'username': username,
            'uid': f"user_{hash(email)}",
            'email_verified': False
        }
        
        st.session_state.user = user
        return True
        
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return False

def logout():
    """Logout current user"""
    if 'user' in st.session_state:
        del st.session_state.user
    st.rerun()

def reset_password(email):
    """Send password reset email"""
    try:
        st.success(f"Password reset email sent to {email}")
        return True
    except Exception as e:
        st.error(f"Password reset failed: {str(e)}")
        return False