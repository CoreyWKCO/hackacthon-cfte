import streamlit as st

# Page config
st.set_page_config(
    page_title="EduSmart • Learning Platform", 
    page_icon="📚", 
    layout="wide"
)

# Modern CSS
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    
    .header {
        text-align: center;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .features-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 0 auto;
        max-width: 1200px;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #f1f3f4;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        flex: 1;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #718096;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    .feature-details {
        text-align: left;
        color: #4a5568;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 2rem;
        padding: 0 0.5rem;
    }
    
    .feature-details ul {
        padding-left: 1.2rem;
        margin: 0.5rem 0;
    }
    
    .feature-details li {
        margin-bottom: 0.3rem;
    }
    
    .feature-button {
        width: 100%;
        padding: 0.8rem;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .feature-button:hover {
        background: #5a6fd8;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Feature pages with detailed explanations
def show_exam_generator():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #2d3748;'>📝 Exam Generator</h1>
        <p style='color: #718096; font-size: 1.1rem;'>Create comprehensive exams automatically from your course materials</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature explanation
    with st.expander("ℹ️ About This Feature", expanded=True):
        st.markdown("""
        **How it works:**
        - Upload your course materials (PDF/textbooks/notes)
        - AI analyzes the content and identifies key concepts
        - Generates various question types automatically
        - Creates balanced exams with different difficulty levels
        
        **Benefits:**
        ✅ Saves hours of manual exam creation
        ✅ Ensures comprehensive topic coverage  
        ✅ Maintains consistent difficulty levels
        ✅ Adapts to different learning objectives
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("📤 Upload Course Material", type=["pdf", "txt"], 
                                       help="Upload your textbook, notes, or course materials")
        
        if uploaded_file is not None:
            st.success(f"✅ **File uploaded:** {uploaded_file.name}")
            st.info(f"📊 **File size:** {uploaded_file.size / 1024:.1f} KB")
    
    with col2:
        exam_title = st.text_input("🎯 Exam Title", value="Midterm Exam")
        num_questions = st.slider("Number of Questions", 5, 50, 15)
        question_types = st.multiselect("Question Types", 
                                      ["Multiple Choice", "Short Answer", "Essay", "True/False", "Problem Solving"],
                                      default=["Multiple Choice", "Short Answer"])
    
    if st.button("🚀 Generate Exam Now", type="primary", use_container_width=True):
        with st.spinner("🔄 AI is analyzing your content and generating questions..."):
            st.success("✅ Exam generated successfully!")
            
            st.markdown("### 📋 Generated Exam Preview")
            st.text_area("Exam Content", 
                        f"""# {exam_title}
                        
**Multiple Choice Questions (8 questions):**
1. What is the main concept discussed in chapter 3?
   A) Option 1    B) Option 2    C) Option 3    D) Option 4

**Short Answer Questions (5 questions):**
1. Explain the key principles of the subject matter...

**Problem Solving (2 questions):**
1. Apply the concepts to solve a real-world scenario...

**Total Points: 100 | Time Allowed: 2 hours**""", 
                        height=400)
    
    st.markdown("---")
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()

def show_evaluator():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #2d3748;'>✔️ Answer Evaluator</h1>
        <p style='color: #718096; font-size: 1.1rem;'>Get detailed feedback and grading for student answers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature explanation
    with st.expander("ℹ️ About This Feature", expanded=True):
        st.markdown("""
        **How it works:**
        - Upload exam questions and student answers
        - AI evaluates content understanding and accuracy
        - Provides detailed feedback and improvement suggestions
        - Generates comprehensive performance reports
        
        **Benefits:**
        ✅ Instant, consistent grading
        ✅ Detailed feedback for each student
        ✅ Identifies knowledge gaps
        ✅ Saves grading time significantly
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Exam Questions")
        questions_file = st.file_uploader("Upload Questions File", type=["txt"], key="questions",
                                        help="Upload a text file with exam questions")
        questions_text = st.text_area("Or enter questions manually:", 
                                    placeholder="1. What is the capital of France?\n2. Explain photosynthesis...", 
                                    height=150)
    
    with col2:
        st.subheader("📝 Student Answers")
        answers_file = st.file_uploader("Upload Answers File", type=["txt"], key="answers",
                                      help="Upload student answers in text format")
        answers_text = st.text_area("Or enter answers manually:", 
                                  placeholder="1. Paris\n2. Photosynthesis is the process...", 
                                  height=150)
    
    if st.button("🎯 Evaluate Answers Now", type="primary", use_container_width=True):
        if (questions_text or questions_file) and (answers_text or answers_file):
            with st.spinner("🔍 AI is evaluating answers and generating feedback..."):
                st.success("✅ Evaluation complete!")
                
                st.markdown("### 📊 Evaluation Results")
                st.text_area("Detailed Feedback", 
                            """**Overall Performance: B+ (85%)**

✅ **Strengths:**
• Excellent understanding of core concepts
• Clear and concise explanations
• Good application of principles

💡 **Areas for Improvement:**
• Provide more specific examples
• Expand on theoretical foundations
• Include relevant case studies

📈 **Recommendations:**
1. Review chapters 3-5 for deeper understanding
2. Practice with additional case studies
3. Focus on application-based questions

**Score: 85/100 | Grade: B+**""", 
                            height=400)
        else:
            st.warning("⚠️ Please provide both questions and answers for evaluation")
    
    st.markdown("---")
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()

def show_study_guide():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #2d3748;'>📚 Study Guide Generator</h1>
        <p style='color: #718096; font-size: 1.1rem;'>Create personalized study materials and learning plans</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature explanation
    with st.expander("ℹ️ About This Feature", expanded=True):
        st.markdown("""
        **How it works:**
        - Specify your subject and learning goals
        - AI creates structured study materials
        - Generates personalized learning schedules
        - Provides resource recommendations
        
        **Benefits:**
        ✅ Personalized learning paths
        ✅ Organized study schedules
        ✅ Comprehensive resource collection
        ✅ Adaptive to your learning style
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("📖 Subject Name", placeholder="e.g., Mathematics, Biology, Computer Science...")
        study_goal = st.selectbox("🎯 Learning Goal", 
                                ["Exam Preparation", "Concept Mastery", "Skill Development", "General Knowledge"])
        study_hours = st.slider("⏱️ Weekly Study Hours", 1, 20, 5)
    
    with col2:
        difficulty = st.selectbox("📊 Current Level", ["Beginner", "Intermediate", "Advanced"])
        timeline = st.selectbox("📅 Study Timeline", ["1 Week", "2 Weeks", "1 Month", "3 Months"])
        focus_areas = st.multiselect("🎯 Focus Areas", 
                                   ["Theory", "Practice Problems", "Case Studies", "Applications", "Review"])
    
    if st.button("🚀 Generate Study Guide Now", type="primary", use_container_width=True):
        if subject:
            with st.spinner("📚 Creating your personalized study guide..."):
                st.success("✅ Study guide created successfully!")
                
                st.markdown(f"### 📖 Study Guide: {subject}")
                st.text_area("Your Personalized Study Plan", 
                            f"""# {subject} - Study Guide
                            
**Learning Goal:** {study_goal}
**Timeline:** {timeline}
**Weekly Hours:** {study_hours} hours

## 📚 Study Schedule:
**Week 1: Foundation Building**
- Day 1-2: Core concepts and definitions
- Day 3-4: Basic principles and theories
- Day 5-7: Practice problems and applications

## 🎯 Key Topics:
1. Fundamental concepts and definitions
2. Core principles and applications
3. Problem-solving techniques
4. Real-world applications

## 📋 Recommended Resources:
• Textbook: "Essential {subject}" 
• Online courses and tutorials
• Practice exercises and worksheets
• Additional reading materials

## 💡 Study Tips:
• Review daily for better retention
• Practice with real examples
• Join study groups for discussion
• Take regular breaks for optimal learning""", 
                            height=400)
        else:
            st.warning("⚠️ Please enter a subject name")
    
    st.markdown("---")
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()

# Home page with 3 taller feature cards
def show_home():
    # Smaller header
    st.markdown("""
    <div class="header">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓</div>
        <h1 style="font-size: 2rem; margin-bottom: 0.5rem; font-weight: 800;">EduSmart</h1>
        <p style="font-size: 1rem; opacity: 0.9;">AI Education Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3 Taller Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Exam Generator</div>
            <div class="feature-desc">Create comprehensive exams from course materials</div>
            <div class="feature-details">
                <ul>
                    <li>Upload PDFs or text files</li>
                    <li>Multiple question types</li>
                    <li>Automatic difficulty balancing</li>
                    <li>Customizable exam parameters</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Creating Exams", key="exam_btn", use_container_width=True):
            st.session_state.current_page = 'exam_generator'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✔️</div>
            <div class="feature-title">Answer Evaluator</div>
            <div class="feature-desc">AI-powered grading and feedback system</div>
            <div class="feature-details">
                <ul>
                    <li>Instant answer evaluation</li>
                    <li>Detailed performance analysis</li>
                    <li>Personalized feedback</li>
                    <li>Improvement recommendations</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Evaluating", key="eval_btn", use_container_width=True):
            st.session_state.current_page = 'evaluator'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Study Guide</div>
            <div class="feature-desc">Personalized learning materials generator</div>
            <div class="feature-details">
                <ul>
                    <li>Custom study schedules</li>
                    <li>Structured learning paths</li>
                    <li>Resource recommendations</li>
                    <li>Progress tracking</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Study Guide", key="study_btn", use_container_width=True):
            st.session_state.current_page = 'study_guide'
            st.rerun()

# Main app
def main():
    if st.session_state.current_page == 'home':
        show_home()
    elif st.session_state.current_page == 'exam_generator':
        show_exam_generator()
    elif st.session_state.current_page == 'evaluator':
        show_evaluator()
    elif st.session_state.current_page == 'study_guide':
        show_study_guide()

if __name__ == "__main__":
    main()