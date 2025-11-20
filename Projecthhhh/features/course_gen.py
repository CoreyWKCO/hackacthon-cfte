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

def generate_course_summary(course_text, summary_type, focus_areas, groq_api_key):
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
        "Authorization": f"Bearer {groq_api_key}",
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

def render(groq_api_key):
    current_user = get_current_user()
    if not current_user:
        st.warning("Please login to access this feature")
        return
    
    # Modern header
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
            if st.button("🚀 Generate Study Guide Now", type="primary", use_container_width=True):
                with st.spinner("📚 Creating your personalized study guide..."):
                    summary_content = generate_course_summary(course_text, summary_type, focus_areas, groq_api_key)
                
                if summary_content:
                    st.balloons()
                    st.success("✅ Study guide created successfully!")
                    
                    # Display summary in a beautiful format
                    st.markdown("---")
                    st.markdown('<div class="resume-box">', unsafe_allow_html=True)
                    st.markdown("### 📚 Your Study Guide")
                    st.markdown(f"**Type:** {summary_type} | **Focus:** {focus_areas if focus_areas else 'All Topics'}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display the summary content
                    st.markdown('<div class="summary-section">', unsafe_allow_html=True)
                    st.write(summary_content)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download option
                    st.download_button(
                        "💾 Download Study Guide",
                        summary_content,
                        file_name=f"study_guide_{summary_type.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                else:
                    st.error("❌ Failed to generate study guide. Please try again.")
        
        else:
            st.info("👆 Upload a course PDF to get started")