import streamlit as st
import requests
from PyPDF2 import PdfReader
import re
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

def correct_exam_with_groq(student_answers, correct_solutions, groq_api_key):
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
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama-3.1-8b-instant",
        "temperature": 0.1,
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

def extract_grade_from_response(response_text):
    """Extract numerical grade from AI response"""
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
            return min(100, max(0, grade))
    return None

def get_grade_class(grade):
    """Get CSS class based on grade"""
    if grade >= 90:
        return "high-grade"
    elif grade >= 70:
        return "medium-grade"
    else:
        return "low-grade"

def render(groq_api_key):
    current_user = get_current_user()
    if not current_user:
        st.warning("Please login to access this feature")
        return
    
    # Modern header
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
    
    # Initialize variables
    student_text = None
    correct_text = None
    
    col1, col2 = st.columns(2)
    
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
    
    # Quick accuracy test
    if student_text is not None and correct_text is not None:
        # Check if files are identical
        if student_text.strip() == correct_text.strip():
            st.warning("⚠️ **Same file detected**: Both uploaded files appear to be identical. Expecting high score.")
        
        # Correction button
        if st.button("🎯 Evaluate Answers Now", type="primary", use_container_width=True):
            with st.spinner("🔍 AI is evaluating answers and generating feedback..."):
                correction_result = correct_exam_with_groq(student_text, correct_text, groq_api_key)
            
            if correction_result:
                st.balloons()
                st.markdown("---")
                st.subheader("📊 Evaluation Results")
                
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