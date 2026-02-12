import streamlit as st
import pandas as pd
from datetime import datetime
import time
from pathlib import Path

# Page Config - MUST BE FIRST
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

# Simple CSS
st.markdown("""
<style>
.main-container {
    background: linear-gradient(135deg, #f5f5dc 0%, #e8e4d9 100%);
    min-height: 100vh;
    padding: 20px;
}
.title {
    color: #800020;
    text-align: center;
    font-size: 3rem;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin: 20px 0;
}
</style>
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
    except:
        pass

def save_assessment_result(result_data):
    try:
        filename = DATA_DIR / "assessment_results.csv"
        df = pd.DataFrame([result_data])
        if filename.exists():
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
    except:
        pass

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
        return {}

questions_data = load_questions()

# Pages
def show_landing():
    st.markdown('<h1 class="title">Welcome to Medanta</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:1.5rem; color:#666;">The Medicity</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Begin Your Journey", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

def show_login():
    col1, col2, col1 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
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
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📚 Employee Handbook")
        st.markdown("[Click here to open handbook](https://online.flippingbook.com/view/652486186/)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Assessments")
        if st.button("Start Assessment", key="assess"):
            st.session_state.page = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏅 JCI Handbook")
        st.markdown("[Click here to open JCI handbook](https://online.flippingbook.com/view/389334287/)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💬 Feedback")
        if st.button("Give Feedback", key="feedback"):
            st.session_state.page = 'feedback'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_assessment():
    if not questions_data:
        st.error("⚠️ Could not load questions. Check Question_bank.xlsx")
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
    st.progress(current_idx / len(module_ids))
    
    correct = 0
    total = len(module['questions'])
    
    for i, q in enumerate(module['questions']):
        st.write(f"**Q{i+1}. {q['Question_Text']}**")
        
        options = []
        for opt in ['Option_A', 'Option_B', 'Option_C', 'Option_D']:
            if pd.notna(q.get(opt)) and str(q.get(opt)).strip():
                options.append(q[opt])
        
        ans = st.radio("Select:", options, key=f"q_{current_idx}_{i}")
        
        if ans == q[f"Option_{q['Correct_Option']}"]:
            correct += 1
    
    if st.button("Submit", type="primary"):
        score = (correct / total) * 100
        if score >= 80:
            st.success(f"✅ Passed! {score:.0f}%")
            save_assessment_result({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user': st.session_state.user.get('name'),
                'module': module['name'],
                'score': score,
                'status': 'PASSED'
            })
            st.session_state.current_module_idx += 1
            time.sleep(2)
            st.rerun()
        else:
            st.error(f"❌ Failed. {score:.0f}%. Need 80%")

def show_feedback():
    st.subheader("Training Feedback")
    with st.form("feedback"):
        feedback_text = st.text_area("Your feedback")
        if st.form_submit_button("Submit"):
            st.success("Thank you!")
            st.session_state.page = 'dashboard'
            st.rerun()

# MAIN
page = st.session_state.page

if page == 'landing':
    show_landing()
elif page == 'login':
    show_login()
elif page == 'dashboard':
    show_dashboard()
elif page == 'assessment':
    show_assessment()
elif page == 'feedback':
    show_feedback()
else:
    show_landing()
