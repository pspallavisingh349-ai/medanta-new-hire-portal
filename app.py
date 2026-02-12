import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import random
import time
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
import plotly.graph_objects as go
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# Page Configuration
st.set_page_config(
    page_title="Medanta New Hire Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Moving Background & Animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

/* Moving Gradient Background */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes rotate3D {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes fadeInUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Main Background */
.main-container {
    background: linear-gradient(-45deg, #f5f5dc, #e8e4d9, #f0ebe0, #e5e0d5);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    min-height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -2;
}

/* Floating Particles */
.particle {
    position: fixed;
    background: radial-gradient(circle, rgba(128,0,32,0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
    z-index: -1;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(128, 0, 32, 0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.8s ease-out;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 60px rgba(128, 0, 32, 0.2);
}

/* Medanta Colors */
.medanta-maroon { color: #800020; }
.medanta-cream { color: #f5f5dc; }
.medanta-gold { color: #d4af37; }

/* 3D Seal Animation */
.seal-3d {
    width: 200px;
    height: 200px;
    animation: rotate3D 20s linear infinite;
    transform-style: preserve-3d;
}

.seal-3d:hover {
    animation-duration: 10s;
}

/* Button Styles */
.medanta-btn {
    background: linear-gradient(135deg, #800020 0%, #a00030 100%);
    color: white;
    border: none;
    padding: 16px 40px;
    border-radius: 50px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(128, 0, 32, 0.3);
    position: relative;
    overflow: hidden;
}

.medanta-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: 0.5s;
}

.medanta-btn:hover::before {
    left: 100%;
}

.medanta-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(128, 0, 32, 0.4);
}

/* Input Fields */
.custom-input {
    background: rgba(255, 255, 255, 0.8);
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 16px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}

.custom-input:focus {
    border-color: #800020;
    box-shadow: 0 0 0 4px rgba(128, 0, 32, 0.1);
    outline: none;
}

/* Progress Bar */
.progress-container {
    background: rgba(128, 0, 32, 0.1);
    border-radius: 20px;
    overflow: hidden;
    height: 12px;
}

.progress-bar {
    background: linear-gradient(90deg, #800020, #d4af37);
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
    position: relative;
    overflow: hidden;
}

.progress-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: shimmer 2s infinite;
}

/* Achievement Cards */
.achievement-card {
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(128, 0, 32, 0.05) 100%);
    border: 1px solid rgba(212, 175, 55, 0.3);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    transition: all 0.4s ease;
}

.achievement-card:hover {
    transform: scale(1.05) rotate(2deg);
    box-shadow: 0 15px 40px rgba(212, 175, 55, 0.2);
}

/* Navigation Pills */
.nav-pill {
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50px;
    padding: 12px 24px;
    margin: 0 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.nav-pill:hover, .nav-pill.active {
    background: #800020;
    color: white;
    border-color: #d4af37;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #f5f5dc;
}

::-webkit-scrollbar-thumb {
    background: #800020;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #600018;
}
</style>

<!-- Floating Particles -->
<div class="particle" style="width: 300px; height: 300px; top: 10%; left: 10%; animation-delay: 0s;"></div>
<div class="particle" style="width: 200px; height: 200px; top: 60%; right: 15%; animation-delay: 2s;"></div>
<div class="particle" style="width: 250px; height: 250px; bottom: 20%; left: 30%; animation-delay: 4s;"></div>
<div class="particle" style="width: 180px; height: 180px; top: 30%; right: 30%; animation-delay: 1s;"></div>

""", unsafe_allow_html=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = {}
if 'current_assessment' not in st.session_state:
    st.session_state.current_assessment = 0
if 'assessment_score' not in st.session_state:
    st.session_state.assessment_score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

# Load Questions from Excel
@st.cache_data
def load_questions():
    try:
        df = pd.read_excel('/mnt/kimi/upload/Question_bank.xlsx')
        df = df[df['Active'] == 'YES']
        assessments = {}
        for assessment in df['Assessment_ID'].unique():
            assessment_df = df[df['Assessment_ID'] == assessment]
            assessments[assessment] = {
                'name': assessment_df['Assessment_Name'].iloc[0],
                'questions': assessment_df.to_dict('records')
            }
        return assessments
    except:
        return {}

questions_data = load_questions()

# Google Sheets Integration
def init_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client
    except:
        return None

def log_to_sheets(sheet_name, data):
    try:
        client = init_google_sheets()
        if client:
            sheet = client.open("Medanta_New_Hire_Data").worksheet(sheet_name)
            sheet.append_row(data)
            return True
    except Exception as e:
        st.error(f"Logging error: {e}")
    return False

# Lottie Animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Animated JCI Seal Component
def render_jci_seal():
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <div class="seal-3d" style="margin: 0 auto; width: 250px; height: 250px; 
             background: radial-gradient(circle at 30% 30%, #ffd700, #d4af37, #b8941f);
             border-radius: 50%; box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4),
             inset 0 -10px 30px rgba(0,0,0,0.2); display: flex; align-items: center; 
             justify-content: center; border: 8px solid #800020; position: relative;">
            <div style="text-align: center; color: #800020; font-weight: bold;">
                <div style="font-size: 14px; letter-spacing: 3px;">JCI ACCREDITED</div>
                <div style="font-size: 48px; margin: 10px 0;">GOLD</div>
                <div style="font-size: 12px;">SEAL OF APPROVAL</div>
            </div>
            <div style="position: absolute; top: -10px; right: -10px; 
                 background: #800020; color: white; border-radius: 50%; 
                 width: 60px; height: 60px; display: flex; align-items: center; 
                 justify-content: center; font-size: 24px; animation: pulse 2s infinite;">★</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Medanta Achievements
MEDANTA_ACHIEVEMENTS = [
    {"icon": "🏆", "title": "JCI Gold Seal", "desc": "3rd Consecutive Accreditation"},
    {"icon": "🌍", "title": "Global Recognition", "desc": "Among World's Best Hospitals"},
    {"icon": "❤️", "title": "5000+ Lives", "desc": "Saved through Organ Transplants"},
    {"icon": "🔬", "title": "Research Excellence", "desc": "1000+ Published Papers"},
    {"icon": "⭐", "title": "NABH Accredited", "desc": "Highest Quality Standards"},
    {"icon": "🤖", "title": "Robotic Surgery", "desc": "Pioneer in Da Vinci Surgery"}
]

# Landing Page
def show_landing():
    # Moving Background Container
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    # Hero Section
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 60px 0; animation: fadeInUp 1s ease-out;">
            <h1 style="font-family: 'Playfair Display', serif; font-size: 4rem; 
                 color: #800020; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                Welcome to Medanta
            </h1>
            <p style="font-size: 1.5rem; color: #666; font-family: 'Inter', sans-serif; 
                 letter-spacing: 3px; text-transform: uppercase;">
                The Medicity
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3D JCI Seal
        render_jci_seal()
        
        # Achievements Carousel
        st.markdown("<div style='padding: 40px 0;'>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, achievement in enumerate(MEDANTA_ACHIEVEMENTS[:3]):
            with cols[idx]:
                st.markdown(f"""
                <div class="achievement-card" style="animation-delay: {idx * 0.2}s;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">{achievement['icon']}</div>
                    <h3 style="color: #800020; margin-bottom: 10px; font-family: 'Playfair Display';">
                        {achievement['title']}
                    </h3>
                    <p style="color: #666; font-size: 0.9rem;">{achievement['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # CTA Buttons
        st.markdown("<div style='text-align: center; padding: 60px 0;'>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Begin Your Journey", key="start_btn", 
                        help="Start your induction process"):
                st.session_state.page = 'login'
                st.rerun()
        
        st.markdown("""
            <p style="text-align: center; color: #800020; margin-top: 20px; 
                 font-style: italic; animation: pulse 2s infinite;">
                "Where Healing Meets Innovation"
            </p>
        </div>
        """, unsafe_allow_html=True)

# Login/Registration Page
def show_login():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 50px;">
            <h2 style="text-align: center; color: #800020; font-family: 'Playfair Display'; 
                 font-size: 2.5rem; margin-bottom: 10px;">
                Join the Medanta Family
            </h2>
            <p style="text-align: center; color: #666; margin-bottom: 40px;">
                Your personalized induction journey awaits
            </p>
        """, unsafe_allow_html=True)
        
        # Tabs for New vs Recurring
        tab1, tab2 = st.tabs(["🆕 New Joiner", "🔄 Recurring Employee"])
        
        with tab1:
            with st.form("new_joiner_form"):
                name = st.text_input("Full Name *", placeholder="Enter your full name",
                                   key="new_name")
                emp_id = st.text_input("Employee ID (if available)", 
                                      placeholder="e.g., MED12345", key="new_empid")
                
                col_cat, col_dept = st.columns(2)
                with col_cat:
                    category = st.selectbox("Department Category *", 
                                          ["Select...", "Administration", "Clinical", 
                                           "Paramedical & Nursing", "Other"])
                with col_dept:
                    department = st.text_input("Department *", 
                                             placeholder="e.g., Cardiology")
                
                email = st.text_input("Email Address *", 
                                    placeholder="name@medanta.org", key="new_email")
                mobile = st.text_input("Mobile Number *", 
                                     placeholder="+91 XXXXX XXXXX", key="new_mobile")
                
                submit_new = st.form_submit_button("✨ Create My Portal", 
                                                  use_container_width=True)
                
                if submit_new:
                    if name and category != "Select..." and department and email and mobile:
                        st.session_state.user = {
                            'type': 'new',
                            'name': name,
                            'emp_id': emp_id or 'Pending',
                            'category': category,
                            'department': department,
                            'email': email,
                            'mobile': mobile,
                            'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        # Log to Google Sheets
                        log_to_sheets("User_Logins", [
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            name, emp_id or 'Pending', category, department, email, mobile, 'New Joiner'
                        ])
                        st.success("🎉 Welcome to Medanta! Redirecting...")
                        time.sleep(1)
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("Please fill all required fields (*)")
        
        with tab2:
            with st.form("recurring_form"):
                rec_email = st.text_input("Registered Email *", 
                                        placeholder="your.email@medanta.org",
                                        key="rec_email")
                rec_submit = st.form_submit_button("🔐 Access Portal", 
                                                  use_container_width=True)
                
                if rec_submit:
                    if rec_email:
                        st.session_state.user = {
                            'type': 'recurring',
                            'email': rec_email,
                            'name': rec_email.split('@')[0],
                            'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        log_to_sheets("User_Logins", [
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            rec_email.split('@')[0], 'N/A', 'N/A', 'N/A', 
                            rec_email, 'N/A', 'Recurring'
                        ])
                        st.success("Welcome back! Redirecting...")
                        time.sleep(1)
                        st.session_state.page = 'dashboard'
                        st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Dashboard
def show_dashboard():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    # Personalized Header
    user_name = st.session_state.user.get('name', 'Colleague')
    
    st.markdown(f"""
    <div style="padding: 30px 0; text-align: center; animation: fadeInUp 0.8s ease-out;">
        <h1 style="font-family: 'Playfair Display'; color: #800020; font-size: 3rem;">
            Namaste, {user_name} 🙏
        </h1>
        <p style="color: #666; font-size: 1.2rem; margin-top: 10px;">
            Your personalized journey at Medanta begins here
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Overview
    progress_col1, progress_col2, progress_col3 = st.columns([1, 2, 1])
    with progress_col2:
        st.markdown("""
        <div class="glass-card" style="padding: 30px; margin-bottom: 40px;">
            <h3 style="color: #800020; text-align: center; margin-bottom: 20px;">
                Your Induction Progress
            </h3>
            <div class="progress-container">
                <div class="progress-bar" style="width: 0%;" id="progressBar"></div>
            </div>
            <p style="text-align: center; color: #666; margin-top: 15px; font-size: 0.9rem;">
                Complete all modules to receive your Passport to Medanta
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Four Main Options
    st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Employee Handbook
        st.markdown("""
        <div class="glass-card" style="padding: 40px; text-align: center; cursor: pointer; 
             transition: all 0.4s ease; height: 300px; display: flex; flex-direction: column; 
             justify-content: center; position: relative; overflow: hidden;">
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; 
                 background: radial-gradient(circle, rgba(128,0,32,0.05) 0%, transparent 70%); 
                 animation: pulse 4s infinite;"></div>
            <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">
                📚
            </div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.8rem; 
                 margin-bottom: 15px;">Employee Handbook</h3>
            <p style="color: #666; font-size: 1rem;">Your complete guide to policies, 
                 benefits, and culture at Medanta</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Handbook", key="handbook_btn", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Assessments
        st.markdown("""
        <div class="glass-card" style="padding: 40px; text-align: center; cursor: pointer; 
             transition: all 0.4s ease; height: 300px; display: flex; flex-direction: column; 
             justify-content: center; background: linear-gradient(135deg, rgba(128,0,32,0.05) 0%, 
             rgba(212,175,55,0.05) 100%);">
            <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite; 
                 animation-delay: 0.5s;">📝</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.8rem; 
                 margin-bottom: 15px;">Assessments</h3>
            <p style="color: #666; font-size: 1rem;">Test your knowledge across 17 modules. 
                 80% required to pass!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Assessment", key="assessment_btn", use_container_width=True):
            st.session_state.page = 'assessment_intro'
            st.rerun()
    
    with col2:
        # JCI Handbook
        st.markdown("""
        <div class="glass-card" style="padding: 40px; text-align: center; cursor: pointer; 
             transition: all 0.4s ease; height: 300px; display: flex; flex-direction: column; 
             justify-content: center; background: linear-gradient(135deg, rgba(212,175,55,0.1) 0%, 
             rgba(128,0,32,0.05) 100%); border: 2px solid rgba(212,175,55,0.3);">
            <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite; 
                 animation-delay: 1s;">🏅</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.8rem; 
                 margin-bottom: 15px;">JCI Handbook</h3>
            <p style="color: #666; font-size: 1rem;">International Patient Safety Goals and 
                 accreditation standards</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open JCI Guide", key="jci_btn", use_container_width=True):
            st.session_state.page = 'jci_handbook'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feedback & Report Card
        st.markdown("""
        <div class="glass-card" style="padding: 40px; text-align: center; cursor: pointer; 
             transition: all 0.4s ease; height: 300px; display: flex; flex-direction: column; 
             justify-content: center;">
            <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite; 
                 animation-delay: 1.5s;">💬</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.8rem; 
                 margin-bottom: 15px;">Feedback & Passport</h3>
            <p style="color: #666; font-size: 1rem;">Share your experience and view your 
                 completion certificate</p>
        </div>
        """, unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("Give Feedback", key="feedback_btn", use_container_width=True):
                st.session_state.page = 'feedback'
                st.rerun()
        with col_f2:
            if st.button("View Passport", key="passport_btn", use_container_width=True):
                st.session_state.page = 'passport'
                st.rerun()

# Assessment Introduction
def show_assessment_intro():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 50px; text-align: center;">
            <div style="font-size: 5rem; margin-bottom: 30px; animation: pulse 2s infinite;">
                🎯
            </div>
            <h2 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.5rem; 
                 margin-bottom: 20px;">Assessment Center</h2>
            <p style="color: #666; font-size: 1.1rem; line-height: 1.8; margin-bottom: 30px;">
                You are about to begin your competency assessments.<br><br>
                <strong style="color: #800020;">📋 Total Modules:</strong> 17<br>
                <strong style="color: #800020;">❓ Total Questions:</strong> 172<br>
                <strong style="color: #800020;">✅ Passing Criteria:</strong> 80%<br>
                <strong style="color: #800020;">🔄 Reattempts:</strong> Unlimited until passed
            </p>
            <div style="background: rgba(128,0,32,0.1); border-left: 4px solid #800020; 
                 padding: 20px; border-radius: 10px; margin: 30px 0; text-align: left;">
                <p style="color: #800020; font-weight: 600; margin-bottom: 10px;">💡 Pro Tips:</p>
                <ul style="color: #666; margin-left: 20px;">
                    <li>Read each question carefully</li>
                    <li>You cannot proceed without passing</li>
                    <li>Take breaks between modules</li>
                    <li>All the best! You've got this! 🌟</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start My Assessment Journey", use_container_width=True):
            st.session_state.page = 'assessment'
            st.session_state.current_assessment = 0
            st.session_state.assessment_score = 0
            st.session_state.answers = {}
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Assessment Page
def show_assessment():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    if not questions_data:
        st.error("Assessment data not loaded. Please check Question_bank.xlsx")
        return
    
    # Get current question
    assessment_ids = list(questions_data.keys())
    current_idx = st.session_state.current_assessment
    
    if current_idx >= len(assessment_ids):
        show_assessment_results()
        return
    
    current_assessment_id = assessment_ids[current_idx]
    assessment_info = questions_data[current_assessment_id]
    questions = assessment_info['questions']
    
    # Progress Header
    progress = (current_idx / len(assessment_ids)) * 100
    st.markdown(f"""
    <div style="padding: 20px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; 
             margin-bottom: 20px;">
            <h2 style="color: #800020; font-family: 'Playfair Display';">
                {assessment_info['name']}
            </h2>
            <span style="background: #800020; color: white; padding: 8px 20px; 
                 border-radius: 20px; font-size: 0.9rem;">
                Module {current_idx + 1} of {len(assessment_ids)}
            </span>
        </div>
        <div class="progress-container" style="margin-bottom: 30px;">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Affirmation Message
    affirmations = [
        "🌟 You're doing amazing! Keep going!",
        "💪 Every question makes you stronger!",
        "🎯 Focus and precision - you've got this!",
        "🏥 Medanta believes in you!",
        "⭐ Excellence is your standard!"
    ]
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: rgba(212,175,55,0.1); 
         border-radius: 15px; margin-bottom: 30px; animation: pulse 3s infinite;">
        <p style="color: #800020; font-weight: 600; margin: 0; font-size: 1.1rem;">
            {random.choice(affirmations)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Questions
    correct_count = 0
    total_answered = 0
    
    for idx, q in enumerate(questions):
        st.markdown(f"""
        <div class="glass-card" style="padding: 30px; margin-bottom: 25px; 
             animation: fadeInUp 0.5s ease-out; animation-delay: {idx * 0.1}s;">
            <h4 style="color: #800020; margin-bottom: 20px; font-size: 1.1rem;">
                Q{idx + 1}. {q['Question_Text']}
            </h4>
        """, unsafe_allow_html=True)
        
        options = []
        option_labels = ['A', 'B', 'C', 'D']
        for i, opt in enumerate(['Option_A', 'Option_B', 'Option_C', 'Option_D']):
            if pd.notna(q.get(opt)) and str(q.get(opt)).strip():
                options.append((option_labels[i], q[opt]))
        
        answer_key = f"q_{current_assessment_id}_{idx}"
        selected = st.radio(
            "Select your answer:",
            [f"{opt[0]}. {opt[1]}" for opt in options],
            key=answer_key,
            label_visibility="collapsed"
        )
        
        if selected:
            selected_letter = selected[0]
            st.session_state.answers[answer_key] = selected_letter
            total_answered += 1
            if selected_letter == q['Correct_Option']:
                correct_count += 1
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Submit Section
    st.markdown("<div style='padding: 30px 0; text-align: center;'>", unsafe_allow_html=True)
    
    if total_answered == len(questions):
        score_pct = (correct_count / len(questions)) * 100
        
        if st.button(f"✅ Submit Module (Score: {score_pct:.0f}%)", 
                    use_container_width=True, type="primary"):
            if score_pct >= 80:
                st.success(f"🎉 Congratulations! You scored {score_pct:.0f}% and passed!")
                st.session_state.assessment_score += correct_count
                st.session_state.current_assessment += 1
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"❌ You scored {score_pct:.0f}%. You need 80% to pass.")
                st.info("🔄 Please review the material and reattempt this module.")
                if st.button("🔄 Reattempt Module", key="reattempt"):
                    st.rerun()
    else:
        st.warning(f"⚠️ Please answer all {len(questions)} questions before submitting.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Assessment Results
def show_assessment_results():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    total_questions = sum(len(v['questions']) for v in questions_data.values())
    final_score = (st.session_state.assessment_score / total_questions) * 100
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 60px; margin: 50px auto; max-width: 800px; 
         text-align: center; border: 3px solid #d4af37;">
        <div style="font-size: 6rem; margin-bottom: 30px; animation: pulse 2s infinite;">
            🏆
        </div>
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 3rem; 
             margin-bottom: 20px;">Assessment Complete!</h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 40px;">
            Congratulations on completing all modules!
        </p>
        <div style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
             padding: 40px; border-radius: 20px; margin: 30px 0;">
            <p style="font-size: 1.2rem; margin-bottom: 10px;">Your Final Score</p>
            <h2 style="font-size: 4rem; margin: 0; font-family: 'Playfair Display';">
                {final_score:.1f}%
            </h2>
            <p style="font-size: 1.1rem; margin-top: 15px; opacity: 0.9;">
                {st.session_state.assessment_score} / {total_questions} correct
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if final_score >= 80:
        st.success("✅ You have successfully passed the induction assessment!")
        st.balloons()
        log_to_sheets("Assessment_Results", [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.user.get('name', 'Unknown'),
            st.session_state.user.get('email', 'Unknown'),
            final_score,
            'PASSED'
        ])
    else:
        st.error("❌ You did not meet the 80% passing criteria.")
        st.info("Please review all modules and reattempt the assessment.")
    
    if st.button("🏠 Return to Dashboard", use_container_width=True):
        st.session_state.assessment_complete = True
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Handbook Viewer
def show_handbook():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 30px 0; text-align: center;">
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.5rem;">
            📚 Employee Handbook
        </h1>
        <p style="color: #666; font-size: 1.1rem;">Your comprehensive guide to Medanta</p>
    </div>
    """, unsafe_allow_html=True)
    
    components.iframe("https://online.flippingbook.com/view/652486186/", 
                     height=700, scrolling=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# JCI Handbook
def show_jci_handbook():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 30px 0; text-align: center;">
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.5rem;">
            🏅 JCI Accreditation Standards
        </h1>
        <p style="color: #666; font-size: 1.1rem;">International Patient Safety Goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    components.iframe("https://online.flippingbook.com/view/389334287/", 
                     height=700, scrolling=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# Feedback Form
def show_feedback():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 30px;">
            <h2 style="color: #800020; font-family: 'Playfair Display'; text-align: center; 
                 font-size: 2.2rem; margin-bottom: 10px;">Training Evaluation</h2>
            <p style="text-align: center; color: #666; margin-bottom: 40px;">
                Your feedback helps us improve
            </p>
        """, unsafe_allow_html=True)
        
        with st.form("feedback_form"):
            trainer_name = st.text_input("Trainer Name")
            training_topic = st.text_input("Training Topic")
            
            st.markdown("<h4 style='color: #800020; margin-top: 30px;'>Rate the Session (1-5)</h4>", 
                       unsafe_allow_html=True)
            
            ratings = {}
            parameters = [
                "Session sequence and flow",
                "Depth of content relevance",
                "Usage of relevant methods",
                "Trainer engagement",
                "Trainer readiness",
                "Effective use of methods",
                "Encouragement of participation",
                "Pace of delivery",
                "Audibility and clarity",
                "Learning outcomes focus"
            ]
            
            cols = st.columns(2)
            for idx, param in enumerate(parameters):
                with cols[idx % 2]:
                    ratings[param] = st.slider(param, 1, 5, 3, key=f"rate_{idx}")
            
            comments = st.text_area("Any other comments", height=100)
            
            submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
            
            if submitted:
                avg_rating = sum(ratings.values()) / len(ratings)
                log_to_sheets("Feedback", [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.user.get('name', 'Unknown'),
                    trainer_name, training_topic, avg_rating, comments
                ])
                st.success("🙏 Thank you for your feedback!")
                time.sleep(2)
                st.session_state.page = 'dashboard'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Passport/Report Card
def show_passport():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 60px; margin: 40px auto; max-width: 900px; 
         background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, 
         rgba(245,245,220,0.9) 100%); border: 3px solid #d4af37; position: relative; 
         overflow: hidden;">
        <div style="position: absolute; top: -100px; right: -100px; width: 300px; height: 300px; 
             background: radial-gradient(circle, rgba(212,175,55,0.2) 0%, transparent 70%); 
             border-radius: 50%;"></div>
        
        <div style="text-align: center; border-bottom: 3px solid #800020; padding-bottom: 30px; 
             margin-bottom: 40px;">
            <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.5rem; 
                 margin-bottom: 10px;">🛂 Passport to Medanta</h1>
            <p style="color: #666; font-size: 1.1rem; letter-spacing: 3px; 
                 text-transform: uppercase;">Official Induction Certificate</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 40px;">
            <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Employee Name</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.4rem;">{user.get('name', 'N/A')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Employee ID</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.4rem;">{user.get('emp_id', 'Pending')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Department</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.4rem;">{user.get('department', 'N/A')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px;">
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Joining Date</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.4rem;">{datetime.now().strftime("%B %d, %Y")}</h3>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
             padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 40px;">
            <p style="font-size: 1.1rem; margin-bottom: 15px; opacity: 0.9;">Induction Status</p>
            <h2 style="font-size: 2.5rem; margin: 0; font-family: 'Playfair Display';">
                ✅ COMPLETED
            </h2>
            <p style="margin-top: 15px; opacity: 0.9;">All modules successfully cleared</p>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 0.9rem; font-style: italic;">
            <p>This certifies that the above named employee has completed the mandatory 
            induction program at Medanta - The Medicity</p>
            <p style="margin-top: 20px; color: #800020; font-weight: 600;">
                Validated by: Learning & Development Department<br>
                Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# Main Router
def main():
    # Add Streamlit components import
    import streamlit.components.v1 as components
    
    page = st.session_state.page
    
    if page == 'landing':
        show_landing()
    elif page == 'login':
        show_login()
    elif page == 'dashboard':
        show_dashboard()
    elif page == 'handbook':
        show_handbook()
    elif page == 'jci_handbook':
        show_jci_handbook()
    elif page == 'assessment_intro':
        show_assessment_intro()
    elif page == 'assessment':
        show_assessment()
    elif page == 'feedback':
        show_feedback()
    elif page == 'passport':
        show_passport()

if __name__ == "__main__":
    main()
