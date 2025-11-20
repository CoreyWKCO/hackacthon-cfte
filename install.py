import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Education Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🎓 AI Education Platform")
st.sidebar.markdown("---")

# User session management
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Navigation based on login status
if st.session_state.logged_in_user:
    st.sidebar.success(f"Welcome, {st.session_state.logged_in_user}!")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in_user = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Main navigation for logged-in users
    page = st.sidebar.radio(
        "Navigate to:",
        [
            "🏠 Home",
            "📝 Exam Generator", 
            "✔️ Exam Corrector",
            "📚 Course Generator",
            "🤖 AI Tutor",
            "📞 Contact",
            "⚙️ Settings"
        ]
    )
else:
    page = "🔐 Login"

# Page routing
if page == "🏠 Home":
    st.title("🏠 Home")
    st.write("Welcome to the AI Education Platform!")
    
elif page == "🔐 Login":
    st.title("🔐 Login / Register")
    
    # Simple login system
    import hashlib
    
    if "users" not in st.session_state:
        st.session_state["users"] = {}
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    mode = st.radio("Select mode:", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button(mode):
        if username.strip() == "" or password.strip() == "":
            st.warning("Username and password cannot be empty")
        else:
            if mode == "Register":
                if username in st.session_state["users"]:
                    st.error("Username already exists")
                else:
                    st.session_state["users"][username] = hash_password(password)
                    st.success(f"User '{username}' registered successfully!")
            else:  # Login
                if username in st.session_state["users"]:
                    if st.session_state["users"][username] == hash_password(password):
                        st.success(f"Logged in as {username}")
                        st.session_state["logged_in_user"] = username
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("Username not found")

# For other pages, show placeholder with login requirement
elif page == "📝 Exam Generator":
    st.title("📝 Exam Generator")
    st.info("This feature will generate exams from course materials")
    st.warning("Please login to access full functionality")
    
elif page == "✔️ Exam Corrector":
    st.title("✔️ Exam Corrector")
    st.info("This feature will automatically correct student exams")
    st.warning("Please login to access full functionality")
    
elif page == "📚 Course Generator":
    st.title("📚 Course Generator")
    st.info("This feature will create preparation courses")
    st.warning("Please login to access full functionality")
    
elif page == "🤖 AI Tutor":
    st.title("🤖 AI Tutor")
    st.info("This feature provides AI-powered tutoring")
    st.warning("Please login to access full functionality")
    
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("Configure your API keys and preferences")
    st.warning("Please login to access full functionality")

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    
    if st.button("Send Message"):
        if not name.strip() or not email.strip() or not message.strip():
            st.warning("Please fill all fields")
        else:
            st.success("Message submitted successfully!")
            st.markdown(f"""
            **Name:** {name}  
            **Email:** {email}  
            **Message:** {message}
            """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Features Overview")
st.sidebar.markdown("""
- **📝 Exam Generation** - Create exams from PDFs
- **✔️ Auto Correction** - Grade student answers  
- **📚 Course Prep** - Generate study materials
- **🤖 AI Tutor** - Get instant answers
- **🔐 Secure Login** - User authentication
""")