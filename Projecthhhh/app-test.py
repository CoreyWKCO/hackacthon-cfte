import streamlit as st
import requests
from PyPDF2 import PdfReader
import hashlib
import time
import re

# ================================
# 🔑 HARDCODED API KEY
# ================================
GROQ_API_KEY = "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"

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
    .exam-box {
        padding: 2rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
# 🔧 CORE FUNCTIONS
# ================================
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text if text.strip() else None
    except Exception as e:
        st.error(f"❌ PDF reading error: {str(e)}")
        return None

def generate_exam_with_groq(course_text, exam_type, num_questions, difficulty):
    """Generate exam using Groq API - FAST MODEL BY DEFAULT"""
    
    # Build prompt based on exam type
    if exam_type == "Multiple Choice":
        prompt = f"""
        Create {num_questions} multiple choice questions from this course content.
        Difficulty: {difficulty}
        
        COURSE CONTENT:
        {course_text[:4000]}
        
        FORMAT EACH QUESTION EXACTLY LIKE THIS:
        Q1. [Clear question that tests understanding]
        A) [Plausible option A]
        B) [Plausible option B] 
        C) [Plausible option C]
        D) [Plausible option D]
        Answer: [Correct letter]
        
        Make sure questions are challenging and test real knowledge.
        """
    elif exam_type == "Mixed Questions":
        prompt = f"""
        Create {num_questions} mixed questions (half multiple choice, half open-ended).
        Difficulty: {difficulty}
        
        COURSE CONTENT:
        {course_text[:4000]}
        
        FORMAT:
        PART 1: MULTIPLE CHOICE QUESTIONS
        Q1. [Question]
        A) [Option A]
        B) [Option B]
        C) [Option C] 
        D) [Option D]
        Answer: [Correct letter]
        
        PART 2: OPEN-ENDED QUESTIONS
        Q1. [Thought-provoking question requiring detailed answer]
        """
    else:  # Essay Questions
        prompt = f"""
        Create {num_questions} essay questions that require critical thinking.
        Difficulty: {difficulty}
        
        COURSE CONTENT:
        {course_text[:4000]}
        
        FORMAT:
        Q1. [Question requiring analysis and detailed response]
        Q2. [Question testing deep understanding of concepts]
        """
    
    # Groq API call - USING CURRENT WORKING MODEL
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",  # CURRENT WORKING MODEL
        "temperature": 0.7,
        "max_tokens": 4000,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

def correct_exam_with_groq(student_answers, correct_solutions):
    """IMPROVED Exam correction with better accuracy"""
    
    prompt = f"""
    CRITICAL: You are an expert examiner. Compare these two texts CAREFULLY and provide an ACCURATE grade.
    
    IMPORTANT INSTRUCTIONS:
    1. Compare the STUDENT ANSWERS with the CORRECT SOLUTIONS line by line
    2. If the content is IDENTICAL or VERY SIMILAR, give a HIGH score (90-100%)
    3. If there are minor differences, give a MEDIUM score (70-89%)
    4. If there are major differences, give a LOW score (below 70%)
    5. BE SPECIFIC about what matches and what doesn't
    
    STUDENT'S ANSWERS:
    {student_answers[:3500]}
    
    CORRECT SOLUTIONS/ANSWER KEY:
    {correct_solutions[:3500]}
    
    ANALYSIS REQUIREMENTS:
    1. First, check if the documents are IDENTICAL - if yes, score should be 100%
    2. Compare key elements: questions, answers, explanations
    3. Look for conceptual understanding, not just exact wording
    4. For multiple choice: check if selected answers match correct ones
    5. For open-ended: check if concepts and key points are covered
    
    FORMAT YOUR RESPONSE EXACTLY AS:
    
    OVERALL GRADE: X/100
    SCORE CATEGORY: [Excellent/Good/Needs Improvement]
    
    DETAILED ANALYSIS:
    [Provide specific comparison points]
    
    STRENGTHS:
    [What the student got right]
    
    AREAS FOR IMPROVEMENT:
    [Specific areas that need work]
    
    FINAL FEEDBACK:
    [Constructive summary]
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",  # USING SAME WORKING MODEL FOR CONSISTENCY
        "temperature": 0.1,  # Lower temperature for more consistent results
        "max_tokens": 4000,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

def generate_course_summary(course_text, summary_type, focus_areas):
    """Generate course summary/resume using Groq API"""
    
    prompt = f"""
    Create a comprehensive {summary_type.lower()} for this course material.
    
    COURSE CONTENT:
    {course_text[:5000]}
    
    FOCUS AREAS: {focus_areas}
    
    FORMAT THE SUMMARY AS:
    
    📚 COURSE OVERVIEW
    [Brief 2-3 sentence description of the entire course]
    
    🎯 KEY LEARNING OBJECTIVES
    • [Objective 1]
    • [Objective 2] 
    • [Objective 3]
    
    📖 MAIN TOPICS COVERED
    • [Topic 1 with brief description]
    • [Topic 2 with brief description]
    • [Topic 3 with brief description]
    
    💡 ESSENTIAL CONCEPTS
    • [Concept 1 - explanation]
    • [Concept 2 - explanation]
    • [Concept 3 - explanation]
    
    🛠️ PRACTICAL APPLICATIONS
    • [Application 1]
    • [Application 2]
    
    📝 STUDY RECOMMENDATIONS
    • [Study tip 1]
    • [Study tip 2]
    
    Make it concise, well-structured, and easy to review. Focus on the most important information for exam preparation.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.5,
        "max_tokens": 3000,
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

def extract_grade_from_response(response_text):
    """Extract numerical grade from AI response"""
    # Look for patterns like "85/100", "Grade: 90", etc.
    patterns = [
        r'(\d{1,3})/100',
        r'grade:\s*(\d{1,3})',
        r'score:\s*(\d{1,3})',
        r'(\d{1,3})\s*out of 100',
        r'(\d{1,3})\s*%'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text.lower())
        if match:
            grade = int(match.group(1))
            return min(100, max(0, grade))  # Ensure grade is between 0-100
    
    # If no pattern found, return None
    return None

def get_grade_class(grade):
    """Get CSS class based on grade"""
    if grade >= 90:
        return "high-grade"
    elif grade >= 70:
        return "medium-grade"
    else:
        return "low-grade"

# ================================
# 🎯 IMPROVED UI CODE
# ================================
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
    # IMPROVED LOGIN/REGISTER PAGE
    st.markdown('<div class="main-header">🔐 Welcome</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("🚀 Login")
        
        # Simple login system
        if "users" not in st.session_state:
            st.session_state["users"] = {}
        
        def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()
        
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", use_container_width=True):
            if login_username.strip() == "" or login_password.strip() == "":
                st.warning("Please fill all fields")
            else:
                if login_username in st.session_state["users"]:
                    if st.session_state["users"][login_username] == hash_password(login_password):
                        st.success(f"Logged in as {login_username}")
                        st.session_state["logged_in_user"] = login_username
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("Username not found")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader("📝 Register")
        
        reg_username = st.text_input("Username", key="reg_user")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", use_container_width=True):
            if reg_username.strip() == "" or reg_password.strip() == "":
                st.warning("Please fill all fields")
            elif reg_password != reg_confirm:
                st.error("Passwords don't match")
            else:
                if reg_username in st.session_state["users"]:
                    st.error("Username already exists")
                else:
                    st.session_state["users"][reg_username] = hash_password(reg_password)
                    st.success(f"User '{reg_username}' registered successfully!")
                    st.info("You can now login with your credentials")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features preview
    st.markdown("---")
    st.subheader("✨ Platform Features")
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    
    with col_feat1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("**📝 Exam Generator**")
        st.markdown("Create custom exams from any course material")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_feat2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("**✔️ Exam Corrector**")
        st.markdown("Automatically grade and provide feedback")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_feat3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("**📚 Course Generator**")
        st.markdown("Create simplified course summaries")
        st.markdown('</div>', unsafe_allow_html=True)

# ================================
# 🚀 IMPROVED EXAM GENERATOR PAGE
# ================================
elif page == "📝 Exam Generator":
    st.title("📝 Exam Generator")
    
    if not st.session_state.logged_in_user:
        st.warning("Please login to access this feature")
    else:
        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 Upload Course Material")
            
            uploaded_file = st.file_uploader(
                "Choose your course PDF",
                type="pdf",
                help="Upload textbooks, slides, or notes"
            )
            
            if uploaded_file:
                with st.spinner("Reading PDF content..."):
                    course_text = extract_text_from_pdf(uploaded_file)
                    
                if course_text:
                    st.success(f"✅ PDF processed! ({len(course_text)} characters)")
                    
                    # Show preview
                    with st.expander("📖 Preview Content"):
                        st.text_area(
                            "Extracted Text",
                            course_text[:1000] + "..." if len(course_text) > 1000 else course_text,
                            height=200,
                            label_visibility="collapsed"
                        )
        
        with col2:
            st.subheader("🎯 Exam Configuration")
            
            if uploaded_file and course_text:
                # Configuration options - SIMPLIFIED (no model choice)
                exam_type = st.radio(
                    "Exam Type:",
                    ["Multiple Choice", "Mixed Questions", "Essay Questions"],
                    horizontal=True
                )
                
                col_config1, col_config2 = st.columns(2)
                with col_config1:
                    num_questions = st.slider(
                        "Number of Questions:",
                        min_value=3,
                        max_value=15,
                        value=8
                    )
                with col_config2:
                    difficulty = st.select_slider(
                        "Difficulty Level:",
                        options=["Easy", "Medium", "Hard"],
                        value="Medium"
                    )
                
                # Generate button
                if st.button("🚀 Generate Exam", type="primary", use_container_width=True):
                    with st.spinner("Creating your exam..."):
                        exam_content = generate_exam_with_groq(
                            course_text, exam_type, num_questions, difficulty
                        )
                    
                    if exam_content:
                        st.balloons()
                        st.success("✅ Exam generated successfully!")
                        
                        # Store exam in session for corrector
                        st.session_state.last_generated_exam = exam_content
                        
                        # Display exam
                        st.markdown("---")
                        st.subheader("📝 Generated Exam")
                        
                        st.markdown('<div class="exam-box">', unsafe_allow_html=True)
                        st.write(exam_content)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download
                        st.download_button(
                            "💾 Download Exam",
                            exam_content,
                            file_name=f"exam_{exam_type.replace(' ', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Failed to generate exam. Please try again.")
            
            else:
                st.info("👆 Upload a PDF file to get started")
                
                # Features showcase
                with st.expander("✨ What you can generate:"):
                    st.markdown("""
                    - **Multiple Choice Exams** - With 4 options each
                    - **Mixed Format** - MC + Open questions  
                    - **Essay Questions** - Critical thinking prompts
                    - **Custom Difficulty** - Easy to Hard level
                    - **Instant Generation** - Powered by AI
                    """)

# ================================
# 🆕 IMPROVED EXAM CORRECTOR PAGE
# ================================
# ================================
# 🆕 IMPROVED EXAM CORRECTOR PAGE
# ================================
elif page == "✔️ Exam Corrector":
    st.title("✔️ Exam Corrector")
    
    if not st.session_state.logged_in_user:
        st.warning("Please login to access this feature")
    else:
        st.info("📊 **Improved Accuracy**: Now uses advanced comparison for precise grading")
        
        # Initialize variables
        student_text = None
        correct_text = None
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Student Answers")
            student_pdf = st.file_uploader(
                "Upload student's exam paper (PDF)",
                type="pdf",
                key="student_pdf"
            )
            
            if student_pdf:
                with st.spinner("Reading student answers..."):
                    student_text = extract_text_from_pdf(student_pdf)
                
                if student_text:
                    st.success(f"✅ Student answers loaded! ({len(student_text)} characters)")
                    
                    with st.expander("👀 Preview Student Answers"):
                        st.text(student_text[:800] + "..." if len(student_text) > 800 else student_text)
        
        with col2:
            st.subheader("📚 Correct Solutions")
            correct_pdf = st.file_uploader(
                "Upload answer key/correct solutions (PDF)",
                type="pdf", 
                key="correct_pdf"
            )
            
            if correct_pdf:
                with st.spinner("Reading correct solutions..."):
                    correct_text = extract_text_from_pdf(correct_pdf)
                
                if correct_text:
                    st.success(f"✅ Solutions loaded! ({len(correct_text)} characters)")
                    
                    with st.expander("👀 Preview Solutions"):
                        st.text(correct_text[:800] + "..." if len(correct_text) > 800 else correct_text)
        
        # Quick accuracy test - NOW USING PROPERLY DEFINED VARIABLES
        if student_text is not None and correct_text is not None:
            # Check if files are identical
            if student_text.strip() == correct_text.strip():
                st.warning("⚠️ **Same file detected**: Both uploaded files appear to be identical. Expecting high score.")
            
            # Correction button
            if st.button("🎯 Grade Exam (Improved Accuracy)", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing answers with enhanced comparison..."):
                    correction_result = correct_exam_with_groq(student_text, correct_text)
                
                if correction_result:
                    st.balloons()
                    st.markdown("---")
                    st.subheader("📊 Grading Results")
                    
                    # Extract and display grade
                    grade = extract_grade_from_response(correction_result)
                    
                    if grade is not None:
                        grade_class = get_grade_class(grade)
                        st.markdown(f'<div class="grade-box {grade_class}">', unsafe_allow_html=True)
                        st.markdown(f"### 🎓 Final Grade: {grade}/100")
                        
                        if grade >= 90:
                            st.markdown("**Excellent!** 🏆")
                        elif grade >= 70:
                            st.markdown("**Good Work!** 👍")
                        else:
                            st.markdown("**Needs Improvement** 📚")
                            
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
                    st.write(correction_result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download results
                    st.download_button(
                        "💾 Download Grading Report",
                        correction_result,
                        file_name="exam_grading_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.error("❌ Failed to grade exam. Please try again.")
        
        elif student_text is None and correct_text is None:
            st.info("👆 Upload both student answers and correct solutions to begin grading")
        
        else:
            st.warning("⚠️ Please upload both files to proceed with grading")
# ================================
# 🆕 COURSE GENERATOR PAGE
# ================================
elif page == "📚 Course Generator":
    st.title("📚 Course Generator")
    
    if not st.session_state.logged_in_user:
        st.warning("Please login to access this feature")
    else:
        st.info("🎓 **Create simplified course summaries and study guides from your course materials**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 Upload Course Material")
            
            uploaded_file = st.file_uploader(
                "Upload your course PDF (textbook, slides, notes)",
                type="pdf",
                help="Upload complete course materials for summary generation"
            )
            
            if uploaded_file:
                with st.spinner("Reading course content..."):
                    course_text = extract_text_from_pdf(uploaded_file)
                
                if course_text:
                    st.success(f"✅ Course material loaded! ({len(course_text)} characters)")
                    
                    with st.expander("👀 Preview Course Content"):
                        st.text(course_text[:1000] + "..." if len(course_text) > 1000 else course_text)
        
        with col2:
            st.subheader("🎯 Summary Configuration")
            
            if uploaded_file and course_text:
                # Summary options
                summary_type = st.radio(
                    "Summary Type:",
                    ["Comprehensive Summary", "Quick Review", "Exam Preparation", "Concept Map"],
                    help="Choose the type of summary you need"
                )
                
                focus_areas = st.text_area(
                    "Specific Focus Areas (optional):",
                    placeholder="e.g., key formulas, important dates, main theories...",
                    help="List specific topics you want to focus on"
                )
                
                # Additional options
                col_opt1, col_opt2 = st.columns(2)
                with col_opt1:
                    include_examples = st.checkbox("Include Examples", value=True)
                with col_opt2:
                    include_study_tips = st.checkbox("Include Study Tips", value=True)
                
                # Generate button
                if st.button("🚀 Generate Course Summary", type="primary", use_container_width=True):
                    with st.spinner("Creating your course summary..."):
                        summary_content = generate_course_summary(course_text, summary_type, focus_areas)
                    
                    if summary_content:
                        st.balloons()
                        st.success("✅ Course summary generated successfully!")
                        
                        # Display summary in a beautiful format
                        st.markdown("---")
                        st.markdown('<div class="resume-box">', unsafe_allow_html=True)
                        st.markdown("### 📚 Your Course Summary")
                        st.markdown(f"**Type:** {summary_type} | **Focus:** {focus_areas if focus_areas else 'All Topics'}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display the summary content
                        st.markdown('<div class="summary-section">', unsafe_allow_html=True)
                        st.write(summary_content)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Additional features
                        col_dl1, col_dl2, col_dl3 = st.columns(3)
                        with col_dl1:
                            st.download_button(
                                "💾 Download Summary",
                                summary_content,
                                file_name=f"course_summary_{summary_type.replace(' ', '_')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        with col_dl2:
                            if st.button("📖 Generate Flashcards", use_container_width=True):
                                st.info("Flashcard feature coming soon!")
                        with col_dl3:
                            if st.button("🎯 Create Quiz", use_container_width=True):
                                st.info("Quiz generator coming soon!")
                    
                    else:
                        st.error("❌ Failed to generate course summary. Please try again.")
            
            else:
                st.info("👆 Upload a course PDF to get started")
                
                # Benefits showcase
                with st.expander("✨ What you'll get:"):
                    st.markdown("""
                    - **📚 Comprehensive Overview** - Key concepts and topics
                    - **🎯 Learning Objectives** - What you need to know
                    - **📖 Main Topics** - Organized by importance
                    - **💡 Essential Concepts** - Core ideas explained simply
                    - **🛠️ Practical Applications** - Real-world usage
                    - **📝 Study Recommendations** - How to study effectively
                    """)

# ================================
# 🎯 ALL OTHER PAGES 
# ================================
elif page == "🤖 AI Tutor":
    st.title("🤖 AI Tutor")
    st.info("This feature provides AI-powered tutoring")
    
    if not st.session_state.logged_in_user:
        st.warning("Please login to access full functionality")
    else:
        st.info("Coming soon: Personalized AI tutoring assistant!")
        
        # Placeholder for AI Tutor
        user_question = st.text_area("Ask your question:", placeholder="Type your academic question here...")
        
        if st.button("Get AI Tutor Help"):
            if user_question:
                st.success("AI Tutor feature coming in the next update!")
            else:
                st.warning("Please enter a question")
    
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("Configure your preferences")
    
    if not st.session_state.logged_in_user:
        st.warning("Please login to access full functionality")
    else:
        st.subheader("User Preferences")
        st.text_input("Display Name", value=st.session_state.logged_in_user)
        st.selectbox("Theme", ["Light", "Dark", "Auto"])
        st.slider("Font Size", 12, 24, 16)
        
        if st.button("Save Preferences"):
            st.success("Preferences saved!")

elif page == "📞 Contact":
    st.title("📞 Contact Us")
    
    col_contact1, col_contact2 = st.columns([2, 1])
    
    with col_contact1:
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        
        if st.button("Send Message", use_container_width=True):
            if not name.strip() or not email.strip() or not message.strip():
                st.warning("Please fill all fields")
            else:
                st.success("Message submitted successfully!")
                st.markdown(f"""
                **Name:** {name}  
                **Email:** {email}  
                **Message:** {message}
                """)
    
    with col_contact2:
        st.markdown("### 📧 Support")
        st.markdown("""
        **Email:** support@aiedu.com  
        **Phone:** +1 (555) 123-4567  
        **Hours:** 9AM-6PM Mon-Fri
        
        We typically respond within 24 hours.
        """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Features Overview")
st.sidebar.markdown("""
- **📝 Exam Generation** - Create exams from PDFs
- **✔️ Auto Correction** - Grade student answers  
- **📚 Course Summaries** - Generate study guides
- **🤖 AI Tutor** - Get instant answers
- **🔐 Secure Login** - User authentication
""")