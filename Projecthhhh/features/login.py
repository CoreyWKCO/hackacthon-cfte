import streamlit as st
from utils.auth import login_user, register_user, reset_password

def render():
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 450px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .login-card h1 {
        color: #333;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .login-card .subtitle {
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .form-group {
        margin-bottom: 1.5rem;
        text-align: left;
    }
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        color: #333;
        font-weight: 600;
    }
    .form-group input {
        width: 100%;
        padding: 1rem;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    .form-group input:focus {
        outline: none;
        border-color: #5f259f;
        box-shadow: 0 0 0 3px rgba(95, 37, 159, 0.1);
    }
    .btn-primary {
        width: 100%;
        padding: 1rem;
        background: linear-gradient(135deg, #5f259f, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(95, 37, 159, 0.3);
    }
    .btn-secondary {
        width: 100%;
        padding: 1rem;
        background: transparent;
        color: #5f259f;
        border: 2px solid #5f259f;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .btn-secondary:hover {
        background: #5f259f;
        color: white;
    }
    .divider {
        margin: 2rem 0;
        border-bottom: 1px solid #e1e5e9;
        position: relative;
    }
    .divider-text {
        background: rgba(255, 255, 255, 0.95);
        padding: 0 1rem;
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        color: #666;
    }
    .forgot-password {
        text-align: center;
        margin-top: 1rem;
    }
    .forgot-password a {
        color: #5f259f;
        text-decoration: none;
        cursor: pointer;
    }
    .error-message {
        background: #fee;
        color: #c33;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #fcc;
    }
    .success-message {
        background: #efe;
        color: #363;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #cfc;
    }
    .clickable-text {
        color: #5f259f;
        text-decoration: underline;
        cursor: pointer;
        text-align: center;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # App logo and title
    st.markdown("<h1>EduAI</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Smart Learning Platform</p>', unsafe_allow_html=True)
    
    # Initialize session state for mode
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    # Mode selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True, 
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    with col2:
        if st.button("Register", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'register' else "secondary"):
            st.session_state.auth_mode = 'register'
            st.rerun()
    
    # Authentication form
    if st.session_state.auth_mode == 'login':
        login_form()
    else:
        register_form()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def login_form():
    # Create form for login
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        #comme quoi rana fahmin
        col1, col2 = st.columns([1, 2])
        with col1:
            remember_me = st.checkbox("Remember me")
        
        # Use form_submit_button for the main submit action
        submit_button = st.form_submit_button("Sign In", use_container_width=True)
    
    # Forgot password button goes OUTSIDE the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Forgot password?", use_container_width=True):
            st.info("Password reset feature would be implemented here")
    
    # Handle form submission
    if submit_button:
        if not email or not password:
            st.error("Please fill in all fields")
        else:
            with st.spinner("Signing in..."):
                if login_user(email, password):
                    st.success("Login successful!")
                    st.rerun()

def register_form():
    # Create form for registration
    with st.form("register_form"):
        username = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        # Use form_submit_button for the main submit action
        submit_button = st.form_submit_button("Create Account", use_container_width=True)
    
    # Handle form submission
    if submit_button:
        if not all([username, email, password, confirm_password]):
            st.error("Please fill in all fields")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters")
        elif not terms:
            st.error("Please accept the terms and conditions")
        else:
            with st.spinner("Creating account..."):
                if register_user(email, password, username):
                    st.success("Account created successfully!")
                    st.rerun()