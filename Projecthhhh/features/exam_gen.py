import streamlit as st
import requests
from PyPDF2 import PdfReader
from utils.auth import get_current_user

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

def generate_exam_with_groq(course_text, exam_type, num_questions, difficulty, groq_api_key):
    """Generate exam using Groq API"""
    
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
    
    # Groq API call
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
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

def render(groq_api_key):
    current_user = get_current_user()
    if not current_user:
        st.warning("Please login to access this feature")
        return
    
    # Modern header
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
        uploaded_file = st.file_uploader("📤 Upload Course Material", type=["pdf"], 
                                       help="Upload your textbook, notes, or course materials")
        
        if uploaded_file is not None:
            st.success(f"✅ **File uploaded:** {uploaded_file.name}")
            st.info(f"📊 **File size:** {uploaded_file.size / 1024:.1f} KB")
            
            with st.spinner("Reading PDF content..."):
                course_text = extract_text_from_pdf(uploaded_file)
                
            if course_text:
                st.success(f"✅ PDF processed! ({len(course_text)} characters)")
                
                with st.expander("📖 Preview Content"):
                    st.text_area(
                        "Extracted Text",
                        course_text[:1000] + "..." if len(course_text) > 1000 else course_text,
                        height=200,
                        label_visibility="collapsed"
                    )
    
    with col2:
        exam_title = st.text_input("🎯 Exam Title", value="Midterm Exam")
        num_questions = st.slider("Number of Questions", 5, 20, 10)
        exam_type = st.radio("Question Types", 
                           ["Multiple Choice", "Mixed Questions", "Essay Questions"],
                           index=0)
        difficulty = st.select_slider("Difficulty Level", 
                                    options=["Easy", "Medium", "Hard"],
                                    value="Medium")
    
    if st.button("🚀 Generate Exam Now", type="primary", use_container_width=True):
        if uploaded_file and course_text:
            with st.spinner("🔄 AI is analyzing your content and generating questions..."):
                exam_content = generate_exam_with_groq(
                    course_text, exam_type, num_questions, difficulty, groq_api_key
                )
            
            if exam_content:
                st.balloons()
                st.success("✅ Exam generated successfully!")
                
                # Store exam in session for corrector
                st.session_state.last_generated_exam = exam_content
                
                st.markdown("### 📋 Generated Exam Preview")
                
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
            st.warning("⚠️ Please upload a PDF file first")