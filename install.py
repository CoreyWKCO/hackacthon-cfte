import streamlit as st
import hashlib

# Page config with modern theme
st.set_page_config(
    page_title="EduAI • Smart Learning", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS that works for both light and dark mode
st.markdown("""
<style>
    /* Base variables for consistent theming */
    :root {
        --primary: #213147;
        --accent: #00C74E;
        --bg-light: #0f1116;
        --bg-card: #1e1e1e;
        --text-primary: #ffffff;
        --text-secondary: #a0a0a0;
        --border: #333333;
    }
    
    /* Main background */
    .main {
        background-color: var(--bg-light);
    }
    
    /* Cards that work in both themes */
    .modern-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        border-color: var(--accent);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Text */
    p, div {
        color: var(--text-secondary) !important;
    }
    
    /* Buttons that work in both themes */
    .stButton>button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: #2d3f5d !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(33, 49, 71, 0.4);
    }
    
    /* Primary accent buttons */
    .primary-btn>button {
        background: var(--accent) !important;
    }
    
    .primary-btn>button:hover {
        background: #00b347 !important;
        box-shadow: 0 6px 20px rgba(0, 199, 78, 0.4);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: var(--bg-card) !important;
        border: 2px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(0, 199, 78, 0.2) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-card);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        padding: 1rem 1.5rem !important;
        color: var(--text-secondary) !important;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* Alerts */
    .stSuccess {
        background: var(--accent) !important;
        color: white !important;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    .stError {
        background: #ef4444 !important;
        color: white !important;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    .stWarning {
        background: #f59e0b !important;
        color: white !important;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    .stInfo {
        background: var(--primary) !important;
        color: white !important;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    /* File uploader */
    .stFileUploader>div>div {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border) !important;
        border-radius: 16px !important;
        color: var(--text-secondary) !important;
    }
    
    .stFileUploader>div>div:hover {
        border-color: var(--accent) !important;
        background: rgba(0, 199, 78, 0.05) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--primary) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: var(--accent) !important;
    }
    
    /* Custom scrollbar for dark mode */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-card);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent);
    }
</style>
""", unsafe_allow_html=True)

# Session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'users' not in st.session_state:
    st.session_state.users = {}

# Authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    if username in st.session_state.users and st.session_state.users[username] == hash_password(password):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        return True
    return False

def register_user(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = hash_password(password)
    return True

# Mock functions for your imports
def ask_ai(prompt):
    return f"🤖 **AI Response:**\n\nThis is a sample response to: '{prompt}'\n\n*To get real AI responses, configure your API key in Settings.*"

def correct_exam(questions_text, answers_text):
    return f"""📝 **Exam Correction Report**

**Questions Analysis:**
{questions_text[:200]}...

**Student Answers Analysis:**
{answers_text[:200]}...

**📊 Overall Assessment:**
✅ **Strengths:** Good understanding of core concepts
✅ **Accuracy:** 85% correct answers
✅ **Completeness:** All questions attempted

**💡 Areas for Improvement:**
- Provide more detailed explanations
- Include specific examples where applicable
- Review technical terminology

**🎯 Detailed Feedback:**
The student demonstrates solid comprehension of the subject matter. Answers are generally accurate but could benefit from more depth and specific examples to strengthen the responses.

**📈 Score: 85/100**
**📚 Grade: B+**
"""

def pdf_to_text(file):
    return f"Sample text extracted from: {file.name}\n\nThis is mock PDF content. In a real application, this would contain the actual text from your uploaded PDF file."

# Main app logic
def main():
    # Dark mode sidebar header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 2rem 1rem; background: rgba(255,255,255,0.1); border-radius: 16px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.2);'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🧠</div>
        <h1 style='color: white; margin: 0; font-size: 1.4rem; font-weight: 700;'>EduAI</h1>
        <p style='color: #00C74E; margin: 0; font-size: 0.8rem; font-weight: 600;'>Smart Learning Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        show_login()
    else:
        show_main_app()

def show_login():
    # Dark mode hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='modern-card'>
            <h1 style='color: white; font-size: 3rem; margin-bottom: 1rem; font-weight: 700;'>Welcome to <span style='color: #00C74E;'>EduAI</span></h1>
            <p style='color: #a0a0a0; font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem;'>
                Transform your learning experience with AI-powered education tools. 
                Generate exams, get instant tutoring, and accelerate your academic journey.
            </p>
            <div style='display: flex; gap: 1rem; margin-top: 2rem;'>
                <div style='flex: 1; text-align: center; padding: 1rem; background: rgba(0, 199, 78, 0.1); border-radius: 12px; border: 1px solid rgba(0, 199, 78, 0.3);'>
                    <div style='font-size: 2rem;'>🚀</div>
                    <p style='color: white; font-weight: 600; margin: 0;'>Smart</p>
                </div>
                <div style='flex: 1; text-align: center; padding: 1rem; background: rgba(33, 49, 71, 0.3); border-radius: 12px; border: 1px solid rgba(33, 49, 71, 0.5);'>
                    <div style='font-size: 2rem;'>⚡</div>
                    <p style='color: white; font-weight: 600; margin: 0;'>Fast</p>
                </div>
                <div style='flex: 1; text-align: center; padding: 1rem; background: rgba(0, 199, 78, 0.1); border-radius: 12px; border: 1px solid rgba(0, 199, 78, 0.3);'>
                    <div style='font-size: 2rem;'>🎯</div>
                    <p style='color: white; font-weight: 600; margin: 0;'>Accurate</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2.5rem; background: #213147; border-radius: 20px; border: 1px solid #333; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🎓</div>
            <h3 style='color: white; margin-bottom: 0.5rem;'>Get Started</h3>
            <p style='color: #00C74E; font-weight: 600; font-size: 0.9rem;'>Join the future of learning</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login/Register tabs
    st.markdown("### 🔐 Access Your Account")
    tab1, tab2 = st.tabs(["🚀 **Sign In**", "✨ **Create Account**"])
    
    with tab1:
        st.markdown("""
        <div class='modern-card'>
            <h3 style='color: white; margin-bottom: 2rem;'>Welcome Back!</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            username = st.text_input("👤 Username", key="login_user", placeholder="Enter your username")
        with col2:
            password = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter your password")
        
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button("🎯 Sign In to Dashboard", use_container_width=True, key="login_btn"):
            if login_user(username, password):
                st.success("🎉 Welcome back! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class='modern-card'>
            <h3 style='color: white; margin-bottom: 2rem;'>Join Our Community!</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            username = st.text_input("👤 Choose Username", key="reg_user", placeholder="Create a username")
        with col2:
            password = st.text_input("🔒 Set Password", type="password", key="reg_pass", placeholder="Create a password")
        
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button("✨ Create Account", use_container_width=True, key="register_btn"):
            if register_user(username, password):
                st.success("✅ Account created! Please sign in.")
            else:
                st.error("⚠️ Username taken. Try another.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def show_main_app():
    # User welcome card
    st.sidebar.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 16px; text-align: center; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.2);'>
        <h3 style='color: white; margin: 0 0 0.5rem 0;'>👋 Welcome back</h3>
        <p style='color: #00C74E; margin: 0; font-weight: 700; font-size: 1.1rem;'>{st.session_state.current_user}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 **Sign Out**", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio("", [
        "🏠 **Dashboard**",
        "📝 **Exam Generator**", 
        "✔️ **Exam Corrector**",
        "📚 **Course Generator**", 
        "🤖 **AI Tutor**",
        "📞 **Contact**",
        "⚙️ **Settings**"
    ])
    
    # Page routing
    if "Dashboard" in page:
        show_home()
    elif "Exam Generator" in page:
        show_exam_generator()
    elif "Exam Corrector" in page:
        show_corrector()
    elif "Course Generator" in page:
        show_course_generator()
    elif "AI Tutor" in page:
        show_ai_tutor()
    elif "Contact" in page:
        show_contact()
    elif "Settings" in page:
        show_settings()

def show_home():
    # Dark mode hero
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem; background: #213147; border-radius: 20px; margin-bottom: 2rem; border: 1px solid #333;'>
        <h1 style='color: white; font-size: 3rem; margin-bottom: 1rem; font-weight: 800;'>EduAI Platform</h1>
        <p style='color: #00C74E; font-size: 1.3rem; font-weight: 700;'>AI-POWERED LEARNING EXPERIENCE</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    st.markdown("### 🚀 Core Features")
    col1, col2, col3 = st.columns(3)
    
    features = [
        {"icon": "📝", "title": "Exam Generator", "desc": "AI-powered exam creation from course materials"},
        {"icon": "✔️", "title": "Auto Corrector", "desc": "Smart grading with detailed feedback"},
        {"icon": "🤖", "title": "AI Tutor", "desc": "24/7 learning assistant"}
    ]
    
    for i, feature in enumerate(features):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class='modern-card' style='text-align: center;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>{feature['icon']}</div>
                <h3 style='color: white; margin-bottom: 1rem;'>{feature['title']}</h3>
                <p style='color: #a0a0a0; line-height: 1.6;'>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# ... (Keep all other page functions the same, they'll inherit the dark mode styling)

def show_exam_generator():
    st.markdown("### 📝 Smart Exam Generator")
    st.markdown("Upload your course materials and let AI create customized exams for you!")
    
    uploaded_file = st.file_uploader("📤 **Upload Course PDF**", type=["pdf"], help="Upload your course material in PDF format")
    
    if uploaded_file is not None:
        with st.expander("📄 **Uploaded File Details**", expanded=True):
            st.success(f"✅ **File:** {uploaded_file.name}")
            st.info(f"📊 **Size:** {uploaded_file.size / 1024:.2f} KB")
        
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        if st.button("🎯 **Generate Exam**", use_container_width=True):
            with st.spinner("🔄 AI is generating your exam... This may take a few moments."):
                text = pdf_to_text(uploaded_file)
                prompt = f"Generate a comprehensive exam based on: {text}"
                exam = ask_ai(prompt)
            
            st.markdown("---")
            st.markdown("### 📋 **Generated Exam**")
            st.text_area("📝 **Exam Content**", exam, height=400, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

def show_corrector():
    st.markdown("### ✔️ AI Exam Corrector")
    st.markdown("Upload exam questions and student answers for automatic correction!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Upload Questions")
        questions_file = st.file_uploader(
            "**Upload Questions File (TXT/PDF):**", 
            type=["txt", "pdf"],
            key="questions_uploader",
            help="Upload a file containing exam questions (one question per line)"
        )
        
        if questions_file is not None:
            st.success(f"✅ **Questions file uploaded:** {questions_file.name}")
            
            if questions_file.type == "text/plain":
                questions_content = questions_file.getvalue().decode("utf-8")
                with st.expander("📋 **Questions Preview**", expanded=True):
                    st.text_area("Questions:", questions_content, height=150, label_visibility="collapsed")
            else:
                st.info("📄 PDF file uploaded - content will be processed automatically")
    
    with col2:
        st.markdown("#### 📝 Upload Student Answers")
        answers_file = st.file_uploader(
            "**Upload Answers File (TXT/PDF):**", 
            type=["txt", "pdf"],
            key="answers_uploader",
            help="Upload a file containing student answers"
        )
        
        if answers_file is not None:
            st.success(f"✅ **Answers file uploaded:** {answers_file.name}")
            
            if answers_file.type == "text/plain":
                answers_content = answers_file.getvalue().decode("utf-8")
                with st.expander("📋 **Answers Preview**", expanded=True):
                    st.text_area("Answers:", answers_content, height=150, label_visibility="collapsed")
            else:
                st.info("📄 PDF file uploaded - content will be processed automatically")
    
    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.button("🎯 **Correct Exam**", use_container_width=True):
        if questions_file is not None and answers_file is not None:
            with st.spinner("🔍 AI is correcting the exam... This may take a moment."):
                if questions_file.type == "text/plain":
                    questions_text = questions_file.getvalue().decode("utf-8")
                else:
                    questions_text = pdf_to_text(questions_file)
                
                if answers_file.type == "text/plain":
                    answers_text = answers_file.getvalue().decode("utf-8")
                else:
                    answers_text = pdf_to_text(answers_file)
                
                result = correct_exam(questions_text, answers_text)
            
            st.markdown("---")
            st.markdown("### 📊 **Exam Correction Results**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📝 Questions Summary")
                st.info(f"**File:** {questions_file.name}")
                st.text_area("Questions Content", questions_text[:500] + "..." if len(questions_text) > 500 else questions_text, 
                           height=150, label_visibility="collapsed")
            
            with col2:
                st.markdown("#### 📝 Answers Summary")
                st.info(f"**File:** {answers_file.name}")
                st.text_area("Answers Content", answers_text[:500] + "..." if len(answers_text) > 500 else answers_text, 
                           height=150, label_visibility="collapsed")
            
            st.markdown("---")
            st.markdown("### 🎯 **AI Correction & Feedback**")
            st.text_area("📋 **Detailed Feedback**", result, height=400, label_visibility="collapsed")
            
        else:
            st.warning("⚠️ Please upload both questions and answers files to proceed with correction.")
    st.markdown("</div>", unsafe_allow_html=True)

def show_course_generator():
    st.markdown("### 📚 Smart Course Generator")
    st.markdown("Create comprehensive study materials for any subject!")
    
    subject = st.text_input("🎯 **Subject Name:**", placeholder="e.g., Machine Learning, Calculus, Biology...")
    
    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.button("🚀 **Generate Course Summary**", use_container_width=True):
        if subject.strip():
            with st.spinner(f"📚 Generating course materials for {subject}..."):
                prompt = f"Create a comprehensive study guide for: {subject}"
                result = ask_ai(prompt)
            
            st.markdown("---")
            st.markdown(f"### 📖 **Course Summary: {subject}**")
            st.text_area("📋 **Study Materials**", result, height=400, label_visibility="collapsed")
        else:
            st.warning("⚠️ Please enter a subject name.")
    st.markdown("</div>", unsafe_allow_html=True)

def show_ai_tutor():
    st.markdown("### 🤖 AI Personal Tutor")
    st.markdown("Ask any question and get instant, detailed explanations!")
    
    question = st.text_area("💭 **Your Question:**", placeholder="Ask anything about your subjects, homework, or concepts...", height=150)
    
    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.button("🎯 **Get AI Answer**", use_container_width=True):
        if question.strip():
            with st.spinner("🤔 AI tutor is thinking..."):
                answer = ask_ai(question)
            
            st.markdown("---")
            st.markdown("### 💡 **AI Tutor Response**")
            st.text_area("📋 **Explanation**", answer, height=300, label_visibility="collapsed")
        else:
            st.warning("⚠️ Please enter your question.")
    st.markdown("</div>", unsafe_allow_html=True)

def show_contact():
    st.markdown("### 📞 Contact Us")
    st.markdown("We'd love to hear from you! Send us your feedback or questions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 **Your Name**", placeholder="Enter your full name")
        email = st.text_input("📧 **Your Email**", placeholder="Enter your email address")
    
    with col2:
        message = st.text_area("💬 **Your Message**", placeholder="Tell us what you think or how we can help...", height=150)
    
    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.button("📤 **Send Message**", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.warning("⚠️ Please fill all fields before sending.")
        else:
            st.success("🎉 Message sent successfully! We'll get back to you soon.")
            st.markdown(f"""
            <div class='modern-card'>
                <h4>📋 Message Summary:</h4>
                <p><strong>👤 Name:</strong> {name}</p>
                <p><strong>📧 Email:</strong> {email}</p>
                <p><strong>💬 Message:</strong> {message}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def show_settings():
    st.markdown("### ⚙️ Platform Settings")
    st.markdown("Configure your AI Education Platform experience.")
    
    st.markdown("#### 🔑 API Configuration")
    api_key = st.text_input("🔐 **Gemini API Key:**", type="password", placeholder="Enter your Gemini API key here...")
    
    st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
    if st.button("💾 **Save Settings**", use_container_width=True):
        st.success("✅ Settings saved successfully for this session!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### ℹ️ About EduAI")
    st.markdown("""
    <div class='modern-card'>
        <p>🎓 <strong>EduAI Platform</strong> - Your intelligent education companion</p>
        <p>🚀 <strong>Version:</strong> 1.0.0</p>
        <p>💡 <strong>Powered by:</strong> Streamlit + AI Technology</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()