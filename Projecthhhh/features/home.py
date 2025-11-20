import streamlit as st
from utils.auth import get_current_user

def render():
    current_user = get_current_user()
    
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
        
        .welcome-message {
            text-align: center;
            margin-bottom: 2rem;
            color: #4a5568;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Welcome header
    if current_user:
        user_display = current_user.get('username', current_user.get('email', 'Learner'))
        st.markdown(f"""
        <div class="header">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓</div>
            <h1 style="font-size: 2rem; margin-bottom: 0.5rem; font-weight: 800;">Welcome back, {user_display}!</h1>
            <p style="font-size: 1rem; opacity: 0.9;">Ready to continue your learning journey?</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="header">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓</div>
            <h1 style="font-size: 2rem; margin-bottom: 0.5rem; font-weight: 800;">EduSmart AI Platform</h1>
            <p style="font-size: 1rem; opacity: 0.9;">Transform your learning experience with AI-powered tools</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 3 Feature cards
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
            st.session_state.current_page = 'corrector'
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
            st.session_state.current_page = 'course_generator'
            st.rerun()
    
    # Additional info for logged out users
    if not current_user:
        st.markdown("---")
        st.info("💡 **Get started**: Create an account or login to access all features and save your progress!")