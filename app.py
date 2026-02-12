import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
from pathlib import Path
import base64

# MUST BE FIRST - Page Config
st.set_page_config(
    page_title="Medanta New Hire Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create data folder
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = {}
if 'current_module_idx' not in st.session_state:
    st.session_state.current_module_idx = 0
if 'assessment_score' not in st.session_state:
    st.session_state.assessment_score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-container {
    background: linear-gradient(-45deg, #f5f5dc, #e8e4d9, #f0ebe0, #e5e0d5);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    min-height: 100vh;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -2;
}

.glass-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(128, 0, 32, 0.1);
    padding: 40px;
    margin: 20px 0;
}

#MainMenu, footer, header {visibility: hidden;}
</style>
<div class="main-container"></div>
""", unsafe_allow_html=True)

# CSV Functions
def save_user_data(user_data):
    try:
        filename = DATA_DIR / "user_logins.csv"
        df = pd.DataFrame([user_data])
        if filename.exists():
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
    except Exception as e:
        st.error(f"Error saving: {e}")

# Load Questions
@st.cache_data
def load_questions():
    try:
        df = pd.read_excel('Question_bank.xlsx')
        df = df[df['Active'] == 'YES']
        assessments = {}
        for assessment in df['Assessment_ID'].unique():
            assessment_df = df[df['Assessment_ID'] == assessment]
            assessments[assessment] = {
                'name': assessment_df['Assessment_Name'].iloc[0],
                'questions': assessment_df.to_dict('records')
            }
        return assessments
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return {}

questions_data = load_questions()

# Pages
def show_landing():
    st.markdown("""
    <div style="text-align: center; padding: 60px 0;">
        <h1 style="font-family: Playfair Display; font-size: 4rem; color: #800020; margin-bottom: 20px;">
            Welcome to Medanta
        </h1>
        <p style="font-size: 1.5rem; color: #666; margin-bottom: 40px;">The Medicity</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Begin Your Journey", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

def show_login():
    col1, col2, col1 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Join Medanta Family")
        
        with st.form("login_form"):
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            dept = st.text_input("Department")
            
            if st.form_submit_button("Submit", use_container_width=True):
                if name and email:
                    save_user_data({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'name': name, 
                        'email': email, 
                        'department': dept
                    })
                    st.session_state.user = {'name': name, 'email': email}
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("Please fill required fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    st.title(f"Welcome {st.session_state.user.get('name', '')} 🙏")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Employee Handbook", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
        if st.button("📝 Assessments", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()
    
    with col2:
        if st.button("🏅 JCI Handbook", use_container_width=True):
            st.session_state.page = 'jci'
            st.rerun()
        if st.button("💬 Feedback", use_container_width=True):
            st.session_state.page = 'feedback'
            st.rerun()

def show_handbook():
    st.subheader("Employee Handbook")
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

def show_jci():
    st.subheader("JCI Handbook")
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

def show_assessment():
    if not questions_data:
        st.error("⚠️ Could not load questions. Please check Question_bank.xlsx file.")
        if st.button("Back"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    module_ids = list(questions_data.keys())
    current_idx = st.session_state.current_module_idx
    
    if current_idx >= len(module_ids):
        st.success("🎉 All assessments complete!")
        if st.button("Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    module = questions_data[module_ids[current_idx]]
    st.subheader(f"Module: {module['name']}")
    st.progress((current_idx / len(module_ids)))
    
    correct = 0
    total = len(module['questions'])
    
    for i, q in enumerate(module['questions']):
        st.markdown(f"**Q{i+1}. {q['Question_Text']}**")
        
        options = []
        for opt in ['Option_A', 'Option_B', 'Option_C', 'Option_D']:
            if pd.notna(q.get(opt)) and str(q.get(opt)).strip():
                options.append(q[opt])
        
        ans = st.radio("Select answer:", options, key=f"q_{current_idx}_{i}")
        
        if ans == q[f"Option_{q['Correct_Option']}"]:
            correct += 1
    
    if st.button("Submit Module", type="primary"):
        score = (correct / total) * 100
        if score >= 80:
            st.success(f"✅ Passed! Score: {score:.0f}%")
            st.session_state.current_module_idx += 1
            time.sleep(2)
            st.rerun()
        else:
            st.error(f"❌ Failed. Score: {score:.0f}%. Need 80% to pass.")
            st.info("Click Submit again to retry this module.")

def show_feedback():
    st.subheader("Training Feedback")
    with st.form("feedback"):
        feedback_text = st.text_area("Your feedback")
        if st.form_submit_button("Submit"):
            st.success("Thank you for your feedback!")
            st.session_state.page = 'dashboard'
            st.rerun()

# MAIN ROUTER
try:
    page = st.session_state.page
    
    if page == 'landing':
        show_landing()
    elif page == 'login':
        show_login()
    elif page == 'dashboard':
        show_dashboard()
    elif page == 'handbook':
        show_handbook()
    elif page == 'jci':
        show_jci()
    elif page == 'assessment':
        show_assessment()
    elif page == 'feedback':
        show_feedback()
    else:
        show_landing()
        
except Exception as e:
    st.error(f"App Error: {str(e)}")
    st.info("Please refresh the page or contact support.")
