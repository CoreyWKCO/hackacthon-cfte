import streamlit as st

# Import feature modules
from features import home, login, exam_gen, corrector, course_gen, contact, settings
from utils.auth import get_current_user, logout

# ================================
# 🔑 HARDCODED API KEY
# ================================
GROQ_API_KEY = "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"

# Page configuration
st.set_page_config(
    page_title="EduSmart • AI Learning Platform",
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
    .exam-box {
        padding: 2rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .grade-box {
        background-color: #e7f3ff;
        border: 2px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .high-grade {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: 2px solid #388E3C;
    }
    .medium-grade {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        border: 2px solid #E65100;
    }
    .low-grade {
        background: linear-gradient(135deg, #F44336, #D32F2F);
        color: white;
        border: 2px solid #B71C1C;
    }
    .resume-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .summary-section {
        background-color: white;
        color: #333;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ================================
# 🎯 MAIN APP LOGIC
# ================================
# Sidebar navigation
st.sidebar.title("🎓 EduSmart Platform")
st.sidebar.markdown("---")

# User session management using new auth system
current_user = get_current_user()

if current_user:
    st.sidebar.success(f"Welcome, {current_user.get('username', current_user.get('email', 'Learner'))}!")
    
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    st.sidebar.markdown("---")
    
    # Main navigation for logged-in users
    page = st.sidebar.radio(
        "Navigate to:",
        [
            "🏠 Home",
            "📝 Exam Generator", 
            "✔️ Answer Evaluator",
            "📚 Study Guide",
            "📞 Contact",
            "⚙️ Settings"
        ]
    )
else:
    page = "🔐 Login"

# Page routing
if page == "🏠 Home":
    home.render()

elif page == "🔐 Login":
    login.render()

elif page == "📝 Exam Generator":
    if current_user:
        exam_gen.render(GROQ_API_KEY)
    else:
        st.warning("Please login to access this feature")

elif page == "✔️ Answer Evaluator":
    if current_user:
        corrector.render(GROQ_API_KEY)
    else:
        st.warning("Please login to access this feature")

elif page == "📚 Study Guide":
    if current_user:
        course_gen.render(GROQ_API_KEY)
    else:
        st.warning("Please login to access this feature")

elif page == "⚙️ Settings":
    if current_user:
        settings.render()
    else:
        st.warning("Please login to access this feature")

elif page == "📞 Contact":
    contact.render()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Features Overview")
st.sidebar.markdown("""
- **📝 Exam Generation** - Create exams from PDFs
- **✔️ Auto Correction** - Grade student answers  
- **📚 Study Guides** - Generate learning materials
- **🔐 Secure Login** - User authentication
""")