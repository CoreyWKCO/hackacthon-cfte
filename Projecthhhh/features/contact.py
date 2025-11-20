import streamlit as st

def render():
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