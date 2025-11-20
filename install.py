import streamlit as st
import hashlib

# Page config with education theme
st.set_page_config(
    page_title="EduSmart • Learning Platform", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional education platform CSS
st.markdown("""
<style>
    /* CSS Variables for both themes */
    [data-theme="light"] {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --bg-sidebar: #1a365d;
        --text-primary: #1a365d;
        --text-secondary: #4a5568;
        --text-sidebar: #ffffff;
        --accent-primary: #2b6cb0;
        --accent-secondary: #2c5282;
        --success: #38a169;
        --border-light: #e2e8f0;
        --border-dark: #cbd5e1;
        --shadow-light: 0 4px 6px rgba(0, 0, 0, 0.05);
        --shadow-dark: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    [data-theme="dark"] {
        --bg-primary: #0f1116;
        --bg-secondary: #1a202c;
        --bg-card: #1a202c;
        --bg-sidebar: #1a365d;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
        --text-sidebar: #ffffff;
        --accent-primary: #4299e1;
        --accent-secondary: #3182ce;
        --success: #48bb78;
        --border-light: #2d3748;
        --border-dark: #4a5568;
        --shadow-light: 0 4px 6px rgba(0, 0, 0, 0.2);
        --shadow-dark: 0 10px 15px rgba(0, 0, 0, 0.3);
    }

    /* Main background */
    .main {
        background: var(--bg-primary);
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    /* Professional education cards */
    .edu-card {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-light);
    }
    
    .edu-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-dark);
        border-color: var(--accent-primary);
    }
    
    /* Headers with education theme */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-family: 'Georgia', 'Times New Roman', serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    h1 {
        border-bottom: 3px solid var(--accent-primary);
        padding-bottom: 0.5rem;
    }
    
    /* Text */
    p, div, span {
        color: var(--text-secondary) !important;
        line-height: 1.6;
    }
    
    /* Professional buttons */
    .stButton>button {
        background: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-light);
    }
    
    .stButton>button:hover {
        background: var(--accent-secondary) !important;
        transform: translateY(-1px);
        box-shadow: var(--shadow-dark);
    }
    
    /* Success buttons */
    .success-btn>button {
        background: var(--success) !important;
    }
    
    .success-btn>button:hover {
        background: #2f855a !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: var(--bg-card) !important;
        border: 2px solid var(--border-light) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-secondary);
        padding: 0.25rem;
        border-radius: 8px;
        border: 1px solid var(--border-light);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 6px !important;
        padding: 1rem 1.5rem !important;
        color: var(--text-secondary) !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-primary) !important;
        color: white !important;
    }
    
    /* Alerts */
    .stSuccess {
        background: var(--success) !important;
        color: white !important;
        border-radius: 8px;
        padding: 1rem;
        border: none;
        border-left: 4px solid #2f855a;
    }
    
    .stError {
        background: #e53e3e !important;
        color: white !important;
        border-radius: 8px;
        padding: 1rem;
        border: none;
        border-left: 4px solid #c53030;
    }
    
    .stWarning {
        background: #ed8936 !important;
        color: white !important;
        border-radius: 8px;
        padding: 1rem;
        border: none;
        border-left: 4px solid #dd6b20;
    }
    
    .stInfo {
        background: var(--accent-primary) !important;
        color: white !important;
        border-radius: 8px;
        padding: 1rem;
        border: none;
        border-left: 4px solid var(--accent-secondary);
    }
    
    /* File uploader */
    .stFileUploader>div>div {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border-dark) !important;
        border-radius: 12px !important;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease;
    }
    
    .stFileUploader>div>div:hover {
        border-color: var(--accent-primary) !important;
        background: rgba(66, 153, 225, 0.05) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: var(--bg-card);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-light);
    }
    
    .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--bg-sidebar) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: var(--accent-primary) !important;
        border-radius: 4px;
    }
    
    /* Feature items */
    .feature-item {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .feature-item:hover {
        border-color: var(--accent-primary);
        transform: translateY(-2px);
        box-shadow: var(--shadow-dark);
    }
    
    /* Badges */
    .badge {
        background: var(--accent-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, var(--bg-sidebar) 0%, #2d3748 100%);
        color: white;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
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

# Professional education functions
def generate_exam_content(course_material):
    return f"""**Exam Generated Successfully**

Based on the course material provided, here's a comprehensive examination:

**Multiple Choice Questions (5 questions):**
1. What is the fundamental concept discussed in the material?
   A) Option 1
   B) Option 2  
   C) Option 3
   D) Option 4

**Short Answer Questions (3 questions):**
1. Explain the key principles covered in the material.

**Problem-Solving (2 questions):**
1. Apply the concepts to solve a practical scenario.

**Total Points: 100**
**Time Allowed: 2 hours**"""

def evaluate_answers(questions, answers):
    return f"""**Evaluation Complete**

**Overall Performance: B+ (85%)**

**Strengths:**
• Good understanding of core concepts
• Clear and concise explanations
• Proper application of principles

**Areas for Improvement:**
• Provide more detailed examples
• Expand on theoretical foundations
• Include relevant case studies

**Detailed Feedback:**
The responses demonstrate solid comprehension of the subject matter. Consider adding more specific examples to strengthen your answers and provide deeper analysis where appropriate.

**Recommendations:**
1. Review chapters 3-5 for deeper understanding
2. Practice with additional case studies
3. Focus on application-based questions"""

def create_study_guide(subject):
    return f"""**Study Guide: {subject}**

**Course Overview:**
This comprehensive study guide covers the essential topics and concepts for {subject}.

**Key Topics:**
1. Fundamental Principles
2. Core Concepts and Theories
3. Practical Applications
4. Case Studies and Examples

**Study Schedule:**
**Week 1-2:** Focus on foundational concepts
**Week 3-4:** Advanced topics and applications  
**Week 5:** Review and practice exams

**Recommended Resources:**
• Textbook: "Essential {subject}" by Academic Press
• Online materials: Course website and supplementary readings
• Practice exercises: Weekly problem sets

**Assessment Preparation:**
• Review key definitions weekly
• Complete all practice problems
• Form study groups for discussion"""

def provide_guidance(question):
    return f"""**Guidance Provided**

Regarding your question about: "{question}"

**Key Points to Consider:**
1. Start with the fundamental definitions
2. Understand the underlying principles
3. Apply concepts to practical scenarios
4. Review related case studies

**Recommended Approach:**
• Break down complex problems into smaller components
• Use diagrams and visual aids where helpful
• Practice with similar examples
• Seek clarification on unclear concepts

**Additional Resources:**
• Chapter 4 of the main textbook
• Online tutorial videos on the topic
• Practice exercises in the workbook"""

def extract_content(file):
    return f"Content extracted from: {file.name}\n\nSample course material text for demonstration purposes."

# Main app logic
def main():
    # Professional sidebar header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 2rem 1rem; background: rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 2rem;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📚</div>
        <h1 style='color: white; margin: 0; font-size: 1.3rem; font-weight: 700;'>EduSmart</h1>
        <p style='color: #a0aec0; margin: 0; font-size: 0.8rem;'>Learning Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        show_login()
    else:
        show_main_app()

def show_login():
    # Professional education platform intro
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='edu-card'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>Welcome to EduSmart</h1>
            <p style='font-size: 1.1rem; margin-bottom: 2rem;'>
                Your comprehensive learning platform for academic excellence. 
                Access study materials, generate assessments, and track your progress 
                in one integrated environment.
            </p>
            <div style='display: flex; gap: 1rem; margin-top: 2rem;'>
                <div class='feature-item'>
                    <div style='font-size: 1.5rem;'>📝</div>
                    <p style='font-weight: 600; margin: 0;'>Assessments</p>
                    <p style='font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Create customized exams</p>
                </div>
                <div class='feature-item'>
                    <div style='font-size: 1.5rem;'>📖</div>
                    <p style='font-weight: 600; margin: 0;'>Study Guides</p>
                    <p style='font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Organized learning materials</p>
                </div>
                <div class='feature-item'>
                    <div style='font-size: 1.5rem;'>📊</div>
                    <p style='font-weight: 600; margin: 0;'>Progress</p>
                    <p style='font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Track your learning journey</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='hero-section'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎓</div>
            <h3 style='margin-bottom: 0.5rem;'>Get Started</h3>
            <p style='color: #a0aec0; font-size: 0.9rem;'>Join our learning community</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login/Register
    st.markdown("### Account Access")
    tab1, tab2 = st.tabs(["**Sign In**", "**Create Account**"])
    
    with tab1:
        st.markdown("""
        <div class='edu-card'>
            <h3 style='margin-bottom: 2rem;'>Welcome Back</h3>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", key="login_pass", placeholder="Enter your password")
        
        st.markdown("<div class='success-btn'>", unsafe_allow_html=True)
        if st.button("Sign In to Platform", use_container_width=True, key="login_btn"):
            if login_user(username, password):
                st.success("Welcome back! Loading your dashboard...")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class='edu-card'>
            <h3 style='margin-bottom: 2rem;'>Create Account</h3>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Choose Username", key="reg_user", placeholder="Create a username")
        password = st.text_input("🔒 Set Password", type="password", key="reg_pass", placeholder="Create a password")
        
        st.markdown("<div class='success-btn'>", unsafe_allow_html=True)
        if st.button("Create Account", use_container_width=True, key="register_btn"):
            if register_user(username, password):
                st.success("Account created successfully! Please sign in.")
            else:
                st.error("Username already exists. Please choose another.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def show_main_app():
    # User welcome
    st.sidebar.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 1.5rem;'>
        <p style='color: white; margin: 0 0 0.5rem 0;'>Welcome back</p>
        <p style='color: #a0aec0; margin: 0; font-weight: 600;'>{st.session_state.current_user}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio("", [
        "🏠 Dashboard",
        "📝 Exam Generator", 
        "✔️ Answer Evaluator",
        "📚 Study Guide", 
        "💬 Learning Support",
        "📞 Contact",
        "⚙️ Settings"
    ])
    
    # Page routing
    if page == "🏠 Dashboard":
        show_home()
    elif page == "📝 Exam Generator":
        show_exam_generator()
    elif page == "✔️ Answer Evaluator":
        show_evaluator()
    elif page == "📚 Study Guide":
        show_study_guide()
    elif page == "💬 Learning Support":
        show_learning_support()
    elif page == "📞 Contact":
        show_contact()
    elif page == "⚙️ Settings":
        show_settings()

def show_home():
    # Professional dashboard
    st.markdown("""
    <div class='hero-section'>
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>EduSmart Learning Platform</h1>
        <p style='font-size: 1.2rem; color: #a0aec0;'>Comprehensive tools for academic success</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-item'>
            <div style='font-size: 2rem;'>📚</div>
            <h3>Study Materials</h3>
            <p>Access organized course content and learning resources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-item'>
            <div style='font-size: 2rem;'>📝</div>
            <h3>Assessments</h3>
            <p>Create and take customized exams and quizzes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-item'>
            <div style='font-size: 2rem;'>📊</div>
            <h3>Progress Tracking</h3>
            <p>Monitor your learning journey and achievements</p>
        </div>
        """, unsafe_allow_html=True)

def show_exam_generator():
    st.markdown("### Exam Generator")
    st.markdown("Create customized assessments from your course materials")
    
    uploaded_file = st.file_uploader("Upload Course Material", type=["pdf", "txt"], help="Upload your course content in PDF or text format")
    
    if uploaded_file is not None:
        with st.expander("File Details", expanded=True):
            st.success(f"File uploaded: {uploaded_file.name}")
        
        if st.button("Generate Exam", use_container_width=True):
            with st.spinner("Creating assessment..."):
                content = extract_content(uploaded_file)
                exam = generate_exam_content(content)
            
            st.markdown("---")
            st.markdown("### Generated Assessment")
            st.text_area("Exam Content", exam, height=400, label_visibility="collapsed")

def show_evaluator():
    st.markdown("### Answer Evaluator")
    st.markdown("Submit questions and answers for comprehensive evaluation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Questions")
        questions_file = st.file_uploader(
            "Upload Questions", 
            type=["txt"],
            key="questions_uploader",
            help="Upload questions in text format"
        )
        
        if questions_file is not None:
            st.success(f"Questions uploaded: {questions_file.name}")
            questions_content = questions_file.getvalue().decode("utf-8")
            with st.expander("Questions Preview"):
                st.text_area("Questions", questions_content, height=150, label_visibility="collapsed")
    
    with col2:
        st.markdown("#### Student Answers")
        answers_file = st.file_uploader(
            "Upload Answers", 
            type=["txt"],
            key="answers_uploader",
            help="Upload student answers in text format"
        )
        
        if answers_file is not None:
            st.success(f"Answers uploaded: {answers_file.name}")
            answers_content = answers_file.getvalue().decode("utf-8")
            with st.expander("Answers Preview"):
                st.text_area("Answers", answers_content, height=150, label_visibility="collapsed")
    
    if st.button("Evaluate Answers", use_container_width=True):
        if questions_file is not None and answers_file is not None:
            with st.spinner("Evaluating responses..."):
                questions_text = questions_file.getvalue().decode("utf-8")
                answers_text = answers_file.getvalue().decode("utf-8")
                result = evaluate_answers(questions_text, answers_text)
            
            st.markdown("---")
            st.markdown("### Evaluation Results")
            st.text_area("Feedback", result, height=400, label_visibility="collapsed")
        else:
            st.warning("Please upload both questions and answers files")

def show_study_guide():
    st.markdown("### Study Guide Generator")
    st.markdown("Create comprehensive study materials for any subject")
    
    subject = st.text_input("Subject Name", placeholder="e.g., Mathematics, Biology, History...")
    
    if st.button("Generate Study Guide", use_container_width=True):
        if subject.strip():
            with st.spinner(f"Creating study guide for {subject}..."):
                result = create_study_guide(subject)
            
            st.markdown("---")
            st.markdown(f"### Study Guide: {subject}")
            st.text_area("Study Materials", result, height=400, label_visibility="collapsed")
        else:
            st.warning("Please enter a subject name")

def show_learning_support():
    st.markdown("### Learning Support")
    st.markdown("Get guidance and clarification on academic topics")
    
    question = st.text_area("Your Question", placeholder="Ask about concepts, problems, or study strategies...", height=150)
    
    if st.button("Get Guidance", use_container_width=True):
        if question.strip():
            with st.spinner("Providing guidance..."):
                answer = provide_guidance(question)
            
            st.markdown("---")
            st.markdown("### Learning Guidance")
            st.text_area("Recommendations", answer, height=300, label_visibility="collapsed")
        else:
            st.warning("Please enter your question")

def show_contact():
    st.markdown("### Contact Support")
    st.markdown("Reach out for technical assistance or platform feedback")
    
    name = st.text_input("Your Name")
    email = st.text_input("Your Email") 
    message = st.text_area("Message", placeholder="Describe your issue or provide feedback...", height=150)
    
    if st.button("Send Message", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.warning("Please fill all fields")
        else:
            st.success("Message sent! We'll respond within 24 hours.")
            st.markdown(f"""
            <div class='edu-card'>
                <h4>Message Summary</h4>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong> {message}</p>
            </div>
            """, unsafe_allow_html=True)

def show_settings():
    st.markdown("### Platform Settings")
    st.markdown("Configure your learning environment")
    
    st.markdown("#### Preferences")
    api_key = st.text_input("API Key (Optional)", type="password", placeholder="Enter any required API key")
    
    if st.button("Save Settings", use_container_width=True):
        st.success("Settings updated successfully")
    
    st.markdown("---")
    st.markdown("#### About EduSmart")
    st.markdown("""
    <div class='edu-card'>
        <p>EduSmart Learning Platform v2.1</p>
        <p>Comprehensive academic tools for students and educators</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()