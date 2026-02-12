import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import random
import time
import os
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Medanta New Hire Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create data folder if not exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Custom CSS with Moving Background & Animations
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

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

@keyframes fadeInUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes slideInRight {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes typewriter {
    from { width: 0; }
    to { width: 100%; }
}

/* Main Background */
.main-container {
    background: linear-gradient(-45deg, #f5f5dc, #e8e4d9, #f0ebe0, #e5e0d5, #faf8f3);
    background-size: 500% 500%;
    animation: gradientMove 20s ease infinite;
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
    background: radial-gradient(circle, rgba(128,0,32,0.08) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 8s ease-in-out infinite;
    z-index: -1;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.4);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(128, 0, 32, 0.08);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.8s ease-out;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 60px rgba(128, 0, 32, 0.15);
}

/* Medanta Colors */
.medanta-maroon { color: #800020; }
.medanta-cream { color: #f5f5dc; }
.medanta-gold { color: #d4af37; }

/* 3D Seal Animation */
.seal-container {
    perspective: 1000px;
    width: 220px;
    height: 220px;
    margin: 0 auto;
}

.seal-3d {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    animation: rotate3D 15s linear infinite;
}

.seal-3d:hover {
    animation-duration: 8s;
}

.seal-face {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ffd700, #d4af37, #b8941f);
    border: 8px solid #800020;
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4),
                inset 0 -10px 30px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    backface-visibility: hidden;
}

.seal-back {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: linear-gradient(135deg, #800020, #a00030);
    border: 8px solid #d4af37;
    transform: rotateY(180deg);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    backface-visibility: hidden;
}

/* Button Styles */
.medanta-btn {
    background: linear-gradient(135deg, #800020 0%, #a00030 100%);
    color: white;
    border: none;
    padding: 18px 45px;
    border-radius: 50px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: all 0.4s ease;
    box-shadow: 0 6px 20px rgba(128, 0, 32, 0.3);
    position: relative;
    overflow: hidden;
    font-size: 1rem;
}

.medanta-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: 0.6s;
}

.medanta-btn:hover::before {
    left: 100%;
}

.medanta-btn:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 15px 40px rgba(128, 0, 32, 0.4);
}

/* Input Fields */
.custom-input {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 18px 24px;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.custom-input:focus {
    border-color: #800020;
    box-shadow: 0 0 0 4px rgba(128, 0, 32, 0.1);
    outline: none;
    transform: translateY(-2px);
}

/* Progress Bar */
.progress-container {
    background: rgba(128, 0, 32, 0.1);
    border-radius: 20px;
    overflow: hidden;
    height: 14px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.progress-bar {
    background: linear-gradient(90deg, #800020, #d4af37, #800020);
    background-size: 200% 100%;
    height: 100%;
    border-radius: 20px;
    transition: width 0.8s ease;
    position: relative;
    overflow: hidden;
    animation: shimmer 3s infinite;
}

/* Achievement Cards */
.achievement-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(245,245,220,0.8) 100%);
    border: 2px solid rgba(212, 175, 55, 0.3);
    border-radius: 24px;
    padding: 35px 25px;
    text-align: center;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.achievement-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #800020, #d4af37);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.achievement-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 50px rgba(128, 0, 32, 0.15);
}

.achievement-card:hover::before {
    transform: scaleX(1);
}

/* Question Cards */
.question-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 25px;
    border-left: 5px solid #800020;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    animation: slideInRight 0.6s ease-out;
}

.question-card:hover {
    transform: translateX(10px);
    box-shadow: 0 8px 30px rgba(128, 0, 32, 0.1);
}

/* Affirmation Banner */
.affirmation-banner {
    background: linear-gradient(135deg, rgba(212,175,55,0.15) 0%, rgba(128,0,32,0.08) 100%);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 35px;
    border: 1px solid rgba(212,175,55,0.3);
    animation: pulse 4s infinite;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #f5f5dc;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #800020, #a00030);
    border-radius: 6px;
    border: 3px solid #f5f5dc;
}

::-webkit-scrollbar-thumb:hover {
    background: #600018;
}

/* Radio Button Styling */
div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.7);
    padding: 15px 20px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    cursor: pointer;
}

div[role="radiogroup"] > label:hover {
    background: rgba(128,0,32,0.05);
    border-color: rgba(128,0,32,0.2);
    transform: translateX(5px);
}

/* Success/Error Messages */
.success-msg {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border-left: 5px solid #28a745;
    padding: 20px;
    border-radius: 12px;
    color: #155724;
    animation: fadeInUp 0.5s ease;
}

.error-msg {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    border-left: 5px solid #dc3545;
    padding: 20px;
    border-radius: 12px;
    color: #721c24;
    animation: shake 0.5s ease;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-10px); }
    75% { transform: translateX(10px); }
}
</style>

<!-- Floating Particles -->
<div class="particle" style="width: 400px; height: 400px; top: 5%; left: 5%; animation-delay: 0s;"></div>
<div class="particle" style="width: 300px; height: 300px; top: 70%; right: 10%; animation-delay: 3s;"></div>
<div class="particle" style="width: 350px; height: 350px; bottom: 10%; left: 40%; animation-delay: 5s;"></div>
<div class="particle" style="width: 250px; height: 250px; top: 40%; right: 30%; animation-delay: 2s;"></div>
<div class="particle" style="width: 200px; height: 200px; top: 20%; left: 70%; animation-delay: 4s;"></div>

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
if 'current_module_idx' not in st.session_state:
    st.session_state.current_module_idx = 0

# CSV Data Management Functions
def save_user_data(user_data):
    """Save user registration data to CSV"""
    filename = DATA_DIR / "user_logins.csv"
    df = pd.DataFrame([user_data])
    if filename.exists():
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def save_assessment_result(result_data):
    """Save assessment results to CSV"""
    filename = DATA_DIR / "assessment_results.csv"
    df = pd.DataFrame([result_data])
    if filename.exists():
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def save_feedback(feedback_data):
    """Save feedback to CSV"""
    filename = DATA_DIR / "feedback.csv"
    df = pd.DataFrame([feedback_data])
    if filename.exists():
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def get_download_link(file_path, link_text):
    """Generate download link for CSV files"""
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{file_path.name}" style="text-decoration: none;"><button class="medanta-btn" style="padding: 12px 30px; font-size: 0.9rem;">{link_text}</button></a>'

# Load Questions from Excel
@st.cache_data
def load_questions():
    try:
        # Try multiple paths
        possible_paths = [
            Path("/mnt/kimi/upload/Question_bank.xlsx"),
            Path("Question_bank.xlsx"),
            Path("data/Question_bank.xlsx")
        ]
        
        for path in possible_paths:
            if path.exists():
                df = pd.read_excel(path)
                df = df[df['Active'] == 'YES']
                assessments = {}
                for assessment in df['Assessment_ID'].unique():
                    assessment_df = df[df['Assessment_ID'] == assessment]
                    assessments[assessment] = {
                        'name': assessment_df['Assessment_Name'].iloc[0],
                        'questions': assessment_df.to_dict('records')
                    }
                return assessments
        return {}
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return {}

questions_data = load_questions()

# Medanta Achievements
MEDANTA_ACHIEVEMENTS = [
    {"icon": "🏆", "title": "JCI Gold Seal", "desc": "3rd Consecutive Accreditation", "detail": "Excellence in Patient Safety"},
    {"icon": "🌍", "title": "Global Recognition", "desc": "Among World's Best Hospitals", "detail": "Newsweek Rankings 2024"},
    {"icon": "❤️", "title": "5000+ Lives", "desc": "Saved through Organ Transplants", "detail": "Largest program in India"},
    {"icon": "🔬", "title": "Research Excellence", "desc": "1000+ Published Papers", "detail": "Advancing medical science"},
    {"icon": "⭐", "title": "NABH Accredited", "desc": "Highest Quality Standards", "detail": "Patient-centric care"},
    {"icon": "🤖", "title": "Robotic Surgery", "desc": "Pioneer in Da Vinci Surgery", "detail": "Minimally invasive precision"}
]

# Animated JCI Seal Component
def render_jci_seal():
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <div class="seal-container">
            <div class="seal-3d">
                <div class="seal-face">
                    <div style="text-align: center; color: #800020;">
                        <div style="font-size: 12px; letter-spacing: 3px; font-weight: 600;">JCI ACCREDITED</div>
                        <div style="font-size: 52px; margin: 8px 0; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">GOLD</div>
                        <div style="font-size: 11px; letter-spacing: 2px;">SEAL OF APPROVAL</div>
                        <div style="margin-top: 10px; font-size: 24px;">★★★</div>
                    </div>
                </div>
                <div class="seal-back">
                    <div style="text-align: center;">
                        <div style="font-size: 14px;">MEDANTA</div>
                        <div style="font-size: 10px; margin-top: 10px;">THE MEDICITY</div>
                        <div style="font-size: 40px; margin-top: 10px;">🏥</div>
                    </div>
                </div>
            </div>
        </div>
        <p style="color: #800020; margin-top: 30px; font-style: italic; font-size: 1.1rem; 
             animation: pulse 3s infinite; font-family: 'Playfair Display';">
            "Excellence in Healthcare"
        </p>
    </div>
    """, unsafe_allow_html=True)

# Landing Page
def show_landing():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    # Hero Section
    col1, col2, col1 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 40px 0; animation: fadeInUp 1s ease-out;">
            <h1 style="font-family: 'Playfair Display', serif; font-size: 4.5rem; 
                 color: #800020; margin-bottom: 15px; text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
                 letter-spacing: 2px;">
                Welcome to Medanta
            </h1>
            <p style="font-size: 1.6rem; color: #666; font-family: 'Inter', sans-serif; 
                 letter-spacing: 4px; text-transform: uppercase; font-weight: 300;">
                The Medicity
            </p>
            <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #800020, #d4af37); 
                 margin: 30px auto; border-radius: 2px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3D JCI Seal
        render_jci_seal()
        
        # Achievements Grid
        st.markdown("<div style='padding: 50px 0;'>", unsafe_allow_html=True)
        
        # Display achievements in 2 rows of 3
        for row in range(2):
            cols = st.columns(3)
            for idx in range(3):
                achievement_idx = row * 3 + idx
                if achievement_idx < len(MEDANTA_ACHIEVEMENTS):
                    achievement = MEDANTA_ACHIEVEMENTS[achievement_idx]
                    with cols[idx]:
                        st.markdown(f"""
                        <div class="achievement-card" style="animation-delay: {achievement_idx * 0.15}s; height: 220px;">
                            <div style="font-size: 3.5rem; margin-bottom: 15px; animation: float 4s ease-in-out infinite; 
                                 animation-delay: {achievement_idx * 0.5}s; filter: drop-shadow(0 5px 15px rgba(0,0,0,0.1));">
                                {achievement['icon']}
                            </div>
                            <h3 style="color: #800020; margin-bottom: 8px; font-family: 'Playfair Display'; font-size: 1.3rem;">
                                {achievement['title']}
                            </h3>
                            <p style="color: #666; font-size: 0.95rem; font-weight: 500; margin-bottom: 5px;">
                                {achievement['desc']}
                            </p>
                            <p style="color: #999; font-size: 0.8rem; font-style: italic;">
                                {achievement['detail']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # CTA Button
        st.markdown("<div style='text-align: center; padding: 60px 0;'>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Begin Your Journey", key="start_btn", 
                        help="Start your induction process", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        
        st.markdown("""
            <p style="text-align: center; color: #800020; margin-top: 30px; 
                 font-style: italic; font-family: 'Playfair Display'; font-size: 1.3rem;
                 text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                "Where Healing Meets Innovation"
            </p>
        </div>
        """, unsafe_allow_html=True)

# Login/Registration Page
def show_login():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 40px;">
            <div style="text-align: center; margin-bottom: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">🙏</div>
                <h2 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.8rem; 
                     margin-bottom: 10px;">Join the Medanta Family</h2>
                <p style="color: #666; font-size: 1.1rem;">Your personalized induction journey awaits</p>
                <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #800020, #d4af37); 
                     margin: 20px auto; border-radius: 2px;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tabs for New vs Recurring
        tab1, tab2 = st.tabs(["🆕 New Joiner", "🔄 Recurring Employee"])
        
        with tab1:
            with st.form("new_joiner_form", clear_on_submit=False):
                name = st.text_input("Full Name *", placeholder="Enter your full name",
                                   key="new_name")
                
                col_id, col_cat = st.columns(2)
                with col_id:
                    emp_id = st.text_input("Employee ID", 
                                          placeholder="If available",
                                          help="Leave blank if not yet assigned")
                with col_cat:
                    category = st.selectbox("Department Category *", 
                                          ["Select...", "Administration", "Clinical", 
                                           "Paramedical & Nursing", "Other"])
                
                department = st.text_input("Department Name *", 
                                         placeholder="e.g., Cardiology, HR, Nursing")
                
                col_email, col_mobile = st.columns(2)
                with col_email:
                    email = st.text_input("Email Address *", 
                                        placeholder="name@medanta.org")
                with col_mobile:
                    mobile = st.text_input("Mobile Number *", 
                                         placeholder="+91 XXXXX XXXXX")
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit_new = st.form_submit_button("✨ Create My Portal", 
                                                  use_container_width=True)
                
                if submit_new:
                    if name and category != "Select..." and department and email and mobile:
                        user_data = {
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'New Joiner',
                            'name': name,
                            'emp_id': emp_id if emp_id else 'Pending',
                            'category': category,
                            'department': department,
                            'email': email,
                            'mobile': mobile
                        }
                        save_user_data(user_data)
                        
                        st.session_state.user = {
                            'type': 'new',
                            'name': name,
                            'emp_id': emp_id if emp_id else 'Pending',
                            'category': category,
                            'department': department,
                            'email': email,
                            'mobile': mobile,
                            'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.success("🎉 Welcome to Medanta! Your journey begins now...")
                        time.sleep(1.5)
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill all required fields (*)")
        
        with tab2:
            with st.form("recurring_form"):
                st.markdown("""
                <div style="text-align: center; padding: 20px 0;">
                    <p style="color: #666; margin-bottom: 20px;">Welcome back! Please verify your identity.</p>
                </div>
                """, unsafe_allow_html=True)
                
                rec_email = st.text_input("Registered Email Address *", 
                                        placeholder="your.email@medanta.org")
                
                st.markdown("<br>", unsafe_allow_html=True)
                rec_submit = st.form_submit_button("🔐 Access Portal", 
                                                  use_container_width=True)
                
                if rec_submit:
                    if rec_email:
                        user_data = {
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'type': 'Recurring',
                            'name': rec_email.split('@')[0],
                            'emp_id': 'N/A',
                            'category': 'N/A',
                            'department': 'N/A',
                            'email': rec_email,
                            'mobile': 'N/A'
                        }
                        save_user_data(user_data)
                        
                        st.session_state.user = {
                            'type': 'recurring',
                            'email': rec_email,
                            'name': rec_email.split('@')[0],
                            'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.success("🎉 Welcome back to Medanta!")
                        time.sleep(1.5)
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error("⚠️ Please enter your email")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Dashboard
def show_dashboard():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    user_name = user.get('name', 'Colleague')
    
    # Personalized Header with Animation
    st.markdown(f"""
    <div style="padding: 40px 0; text-align: center; animation: fadeInUp 0.8s ease-out;">
        <div style="font-size: 3.5rem; margin-bottom: 15px; animation: pulse 3s infinite; display: inline-block;">🙏</div>
        <h1 style="font-family: 'Playfair Display'; color: #800020; font-size: 3.2rem; margin-bottom: 10px;">
            Namaste, {user_name}
        </h1>
        <p style="color: #666; font-size: 1.2rem; margin-top: 10px; font-weight: 300;">
            Your personalized journey at Medanta begins here
        </p>
        <div style="width: 120px; height: 4px; background: linear-gradient(90deg, #800020, #d4af37); 
             margin: 25px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Overview
    progress_col1, progress_col2, progress_col1 = st.columns([0.5, 3, 0.5])
    with progress_col2:
        st.markdown("""
        <div class="glass-card" style="padding: 35px; margin-bottom: 50px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="color: #800020; margin: 0; font-family: 'Playfair Display'; font-size: 1.4rem;">
                    Your Induction Progress
                </h3>
                <span style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
                     padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; font-weight: 500;">
                    In Progress
                </span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: 25%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 15px; color: #666; font-size: 0.9rem;">
                <span>Started</span>
                <span>25% Complete</span>
                <span>Passport</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Four Main Options
    st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Employee Handbook
        st.markdown("""
        <div class="glass-card" style="padding: 45px; text-align: center; height: 320px; 
             display: flex; flex-direction: column; justify-content: center; position: relative; 
             overflow: hidden; background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, 
             rgba(245,245,220,0.7) 100%);">
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; 
                 background: radial-gradient(circle, rgba(128,0,32,0.03) 0%, transparent 70%); 
                 animation: pulse 6s infinite;"></div>
            <div style="font-size: 4.5rem; margin-bottom: 25px; animation: float 4s ease-in-out infinite;
                 filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));">📚</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.9rem; 
                 margin-bottom: 15px; position: relative; z-index: 1;">Employee Handbook</h3>
            <p style="color: #666; font-size: 1.05rem; line-height: 1.6; position: relative; z-index: 1;">
                Your complete guide to policies, benefits, and culture at Medanta
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📖 Read Handbook", key="handbook_btn", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Assessments
        st.markdown("""
        <div class="glass-card" style="padding: 45px; text-align: center; height: 320px; 
             display: flex; flex-direction: column; justify-content: center; 
             background: linear-gradient(135deg, rgba(128,0,32,0.08) 0%, rgba(212,175,55,0.05) 100%);
             border: 2px solid rgba(128,0,32,0.1);">
            <div style="font-size: 4.5rem; margin-bottom: 25px; animation: float 4s ease-in-out infinite; 
                 animation-delay: 0.5s; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));">📝</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.9rem; 
                 margin-bottom: 15px;">Assessments</h3>
            <p style="color: #666; font-size: 1.05rem; line-height: 1.6;">
                Test your knowledge across 17 modules.<br>
                <strong style="color: #800020;">80% required to pass!</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Start Assessment", key="assessment_btn", use_container_width=True):
            st.session_state.page = 'assessment_intro'
            st.rerun()
    
    with col2:
        # JCI Handbook
        st.markdown("""
        <div class="glass-card" style="padding: 45px; text-align: center; height: 320px; 
             display: flex; flex-direction: column; justify-content: center; 
             background: linear-gradient(135deg, rgba(212,175,55,0.12) 0%, rgba(128,0,32,0.05) 100%); 
             border: 2px solid rgba(212,175,55,0.3);">
            <div style="font-size: 4.5rem; margin-bottom: 25px; animation: float 4s ease-in-out infinite; 
                 animation-delay: 1s; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));">🏅</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.9rem; 
                 margin-bottom: 15px;">JCI Handbook</h3>
            <p style="color: #666; font-size: 1.05rem; line-height: 1.6;">
                International Patient Safety Goals and accreditation standards
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏅 Open JCI Guide", key="jci_btn", use_container_width=True):
            st.session_state.page = 'jci_handbook'
            st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Feedback & Report Card
        st.markdown("""
        <div class="glass-card" style="padding: 45px; text-align: center; height: 320px; 
             display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4.5rem; margin-bottom: 25px; animation: float 4s ease-in-out infinite; 
                 animation-delay: 1.5s; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));">💼</div>
            <h3 style="color: #800020; font-family: 'Playfair Display'; font-size: 1.9rem; 
                 margin-bottom: 15px;">Feedback & Passport</h3>
            <p style="color: #666; font-size: 1.05rem; line-height: 1.6;">
                Share your experience and view your completion certificate
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("💬 Feedback", key="feedback_btn", use_container_width=True):
                st.session_state.page = 'feedback'
                st.rerun()
        with col_f2:
            if st.button("🎓 Passport", key="passport_btn", use_container_width=True):
                st.session_state.page = 'passport'
                st.rerun()
    
    # Admin Section - Download Data
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🔐 Admin: Download Reports (HR Only)"):
        st.markdown("""
        <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px; margin-top: 15px;">
            <h4 style="color: #800020; margin-bottom: 15px;">Download Audit Reports</h4>
            <p style="color: #666; margin-bottom: 20px; font-size: 0.95rem;">
                All data is automatically saved to CSV files. Click below to download:
            </p>
        """, unsafe_allow_html=True)
        
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            if (DATA_DIR / "user_logins.csv").exists():
                st.markdown(get_download_link(DATA_DIR / "user_logins.csv", "📥 User Logins"), 
                           unsafe_allow_html=True)
            else:
                st.info("No data yet")
        
        with col_d2:
            if (DATA_DIR / "assessment_results.csv").exists():
                st.markdown(get_download_link(DATA_DIR / "assessment_results.csv", "📥 Assessment Results"), 
                           unsafe_allow_html=True)
            else:
                st.info("No data yet")
        
        with col_d3:
            if (DATA_DIR / "feedback.csv").exists():
                st.markdown(get_download_link(DATA_DIR / "feedback.csv", "📥 Feedback"), 
                           unsafe_allow_html=True)
            else:
                st.info("No data yet")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Assessment Introduction
def show_assessment_intro():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 40px; text-align: center;">
            <div style="font-size: 5rem; margin-bottom: 30px; animation: pulse 2s infinite; display: inline-block;">
                🎯
            </div>
            <h2 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.8rem; 
                 margin-bottom: 20px;">Assessment Center</h2>
            <p style="color: #666; font-size: 1.15rem; line-height: 1.8; margin-bottom: 35px;">
                You are about to begin your competency assessments.<br>
                Prepare yourself for an engaging learning experience.
            </p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 35px 0;">
                <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">📋</div>
                    <div style="color: #800020; font-weight: 600; font-size: 1.3rem;">17 Modules</div>
                    <div style="color: #666; font-size: 0.9rem;">Comprehensive coverage</div>
                </div>
                <div style="background: rgba(128,0,32,0.05); padding: 25px; border-radius: 15px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">❓</div>
                    <div style="color: #800020; font-weight: 600; font-size: 1.3rem;">172 Questions</div>
                    <div style="color: #666; font-size: 0.9rem;">Total assessment</div>
                </div>
                <div style="background: rgba(212,175,55,0.1); padding: 25px; border-radius: 15px; text-align: center; border: 2px solid rgba(212,175,55,0.3);">
                    <div style="font-size: 2rem; margin-bottom: 10px;">✅</div>
                    <div style="color: #800020; font-weight: 600; font-size: 1.3rem;">80% Pass</div>
                    <div style="color: #666; font-size: 0.9rem;">Required to proceed</div>
                </div>
                <div style="background: rgba(212,175,55,0.1); padding: 25px; border-radius: 15px; text-align: center; border: 2px solid rgba(212,175,55,0.3);">
                    <div style="font-size: 2rem; margin-bottom: 10px;">🔄</div>
                    <div style="color: #800020; font-weight: 600; font-size: 1.3rem;">Unlimited</div>
                    <div style="color: #666; font-size: 0.9rem;">Reattempts allowed</div>
                </div>
            </div>
            
            <div style="background: linear-gradient(135deg, rgba(128,0,32,0.08), rgba(212,175,55,0.08)); 
                 border-left: 5px solid #800020; padding: 25px; border-radius: 12px; 
                 margin: 35px 0; text-align: left;">
                <p style="color: #800020; font-weight: 600; margin-bottom: 15px; font-size: 1.1rem;">
                    💡 Pro Tips for Success:
                </p>
                <ul style="color: #555; margin-left: 20px; line-height: 2;">
                    <li>Read each question carefully before answering</li>
                    <li>You must pass each module to unlock the next</li>
                    <li>Take breaks between modules if needed</li>
                    <li>Stay positive - you can reattempt if needed!</li>
                    <li>All the best! Medanta believes in you! 🌟</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start My Assessment Journey", use_container_width=True):
            st.session_state.page = 'assessment'
            st.session_state.current_module_idx = 0
            st.session_state.assessment_score = 0
            st.session_state.answers = {}
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Assessment Page
def show_assessment():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    if not questions_data:
        st.error("⚠️ Assessment data not loaded. Please ensure Question_bank.xlsx is in the same folder.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    # Get modules
    module_ids = list(questions_data.keys())
    current_module_idx = st.session_state.current_module_idx
    
    if current_module_idx >= len(module_ids):
        show_assessment_results()
        return
    
    current_module_id = module_ids[current_module_idx]
    module_info = questions_data[current_module_id]
    questions = module_info['questions']
    
    # Progress Header
    progress = ((current_module_idx) / len(module_ids)) * 100
    st.markdown(f"""
    <div style="padding: 25px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <div>
                <h2 style="color: #800020; font-family: 'Playfair Display'; margin: 0; font-size: 2rem;">
                    {module_info['name']}
                </h2>
                <p style="color: #666; margin: 8px 0 0 0; font-size: 0.95rem;">Module {current_module_idx + 1} of {len(module_ids)}</p>
            </div>
            <span style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
                 padding: 12px 25px; border-radius: 25px; font-size: 0.95rem; font-weight: 500; 
                 box-shadow: 0 4px 15px rgba(128,0,32,0.3);">
                {len(questions)} Questions
            </span>
        </div>
        <div class="progress-container" style="margin-bottom: 15px; height: 16px;">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        <p style="text-align: right; color: #666; font-size: 0.9rem; margin: 0;">
            Overall Progress: {progress:.0f}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Affirmation Message
    affirmations = [
        "🌟 You're doing amazing! Keep going!",
        "💪 Every question makes you stronger!",
        "🎯 Focus and precision - you've got this!",
        "🏥 Medanta believes in you!",
        "⭐ Excellence is your standard!",
        "🚀 You're closer to your goal!",
        "💡 Trust your knowledge!",
        "🏆 Success is within reach!"
    ]
    
    current_affirmation = affirmations[current_module_idx % len(affirmations)]
    
    st.markdown(f"""
    <div class="affirmation-banner">
        <p style="color: #800020; font-weight: 600; margin: 0; font-size: 1.15rem; letter-spacing: 0.5px;">
            {current_affirmation}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Questions
    correct_count = 0
    total_answered = 0
    
    for idx, q in enumerate(questions):
        st.markdown(f"""
        <div class="question-card" style="animation-delay: {idx * 0.1}s;">
            <h4 style="color: #800020; margin-bottom: 25px; font-size: 1.15rem; line-height: 1.6; font-weight: 500;">
                <span style="background: #800020; color: white; padding: 5px 12px; border-radius: 20px; 
                     font-size: 0.85rem; margin-right: 12px; display: inline-block;">Q{idx + 1}</span>
                {q['Question_Text']}
            </h4>
        """, unsafe_allow_html=True)
        
        options = []
        option_labels = ['A', 'B', 'C', 'D']
        for i, opt in enumerate(['Option_A', 'Option_B', 'Option_C', 'Option_D']):
            if pd.notna(q.get(opt)) and str(q.get(opt)).strip():
                options.append((option_labels[i], q[opt]))
        
        answer_key = f"q_{current_module_id}_{idx}"
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
    st.markdown("<div style='padding: 40px 0; text-align: center;'>", unsafe_allow_html=True)
    
    if total_answered == len(questions):
        score_pct = (correct_count / len(questions)) * 100
        
        col_btn1, col_btn2, col_btn1 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button(f"✅ Submit Module (Current Score: {score_pct:.0f}%)", 
                        use_container_width=True, type="primary"):
                if score_pct >= 80:
                    st.balloons()
                    st.success(f"🎉 Excellent! You scored {score_pct:.0f}% and passed!")
                    
                    # Save progress
                    result_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'user': st.session_state.user.get('name', 'Unknown'),
                        'email': st.session_state.user.get('email', 'Unknown'),
                        'module': module_info['name'],
                        'score': score_pct,
                        'correct': correct_count,
                        'total': len(questions),
                        'status': 'PASSED'
                    }
                    save_assessment_result(result_data)
                    
                    time.sleep(2)
                    st.session_state.assessment_score += correct_count
                    st.session_state.current_module_idx += 1
                    st.rerun()
                else:
                    st.error(f"❌ You scored {score_pct:.0f}%. You need 80% to pass this module.")
                    st.info("💪 Don't worry! Review the material and try again. You can do this!")
                    
                    if st.button("🔄 Reattempt This Module", key="reattempt"):
                        st.rerun()
    else:
        remaining = len(questions) - total_answered
        st.warning(f"⚠️ Please answer all questions. {remaining} remaining.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Assessment Results
def show_assessment_results():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    total_questions = sum(len(v['questions']) for v in questions_data.values())
    final_score = (st.session_state.assessment_score / total_questions) * 100
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 60px; margin: 50px auto; max-width: 850px; 
         text-align: center; border: 3px solid #d4af37; background: linear-gradient(135deg, 
         rgba(255,255,255,0.95) 0%, rgba(245,245,220,0.9) 100%); position: relative; overflow: hidden;">
        
        <div style="position: absolute; top: -150px; right: -150px; width: 400px; height: 400px; 
             background: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 70%); 
             border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -100px; left: -100px; width: 300px; height: 300px; 
             background: radial-gradient(circle, rgba(128,0,32,0.08) 0%, transparent 70%); 
             border-radius: 50%;"></div>
        
        <div style="font-size: 6rem; margin-bottom: 30px; animation: pulse 2s infinite; display: inline-block; 
             filter: drop-shadow(0 10px 30px rgba(212,175,55,0.4));">
            🏆
        </div>
        
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 3.2rem; 
             margin-bottom: 15px; position: relative; z-index: 1;">Assessment Complete!</h1>
        
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 40px; position: relative; z-index: 1;">
            Congratulations on completing all modules! You've shown excellence.
        </p>
        
        <div style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
             padding: 50px; border-radius: 25px; margin: 40px 0; position: relative; z-index: 1;
             box-shadow: 0 20px 60px rgba(128,0,32,0.3);">
            <p style="font-size: 1.2rem; margin-bottom: 15px; opacity: 0.9; letter-spacing: 2px; text-transform: uppercase;">
                Your Final Score
            </p>
            <h2 style="font-size: 5rem; margin: 0; font-family: 'Playfair Display'; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                {final_score:.1f}%
            </h2>
            <p style="font-size: 1.2rem; margin-top: 20px; opacity: 0.9;">
                {st.session_state.assessment_score} / {total_questions} correct answers
            </p>
            <div style="width: 100px; height: 4px; background: rgba(255,255,255,0.5); margin: 25px auto; border-radius: 2px;"></div>
            <p style="font-size: 1rem; opacity: 0.8; margin: 0;">
                All 17 modules completed successfully
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if final_score >= 80:
        st.success("✅ You have successfully passed the induction assessment! Welcome to Medanta!")
        st.balloons()
        
        # Save final result
        final_result = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user': st.session_state.user.get('name', 'Unknown'),
            'email': st.session_state.user.get('email', 'Unknown'),
            'final_score': final_score,
            'total_correct': st.session_state.assessment_score,
            'total_questions': total_questions,
            'status': 'COMPLETED'
        }
        save_assessment_result(final_result)
        
        st.session_state.assessment_complete = True
    else:
        st.error("❌ You did not meet the 80% passing criteria overall.")
        st.info("Please review all modules and reattempt. We believe in your success!")
    
    col_btn1, col_btn2, col_btn1 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🏠 Return to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Handbook Viewer
def show_handbook():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 30px 0; text-align: center;">
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.8rem; margin-bottom: 10px;">
            📚 Employee Handbook
        </h1>
        <p style="color: #666; font-size: 1.1rem;">Your comprehensive guide to Medanta</p>
        <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #800020, #d4af37); 
             margin: 20px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/", 
                           height=750, scrolling=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# JCI Handbook
def show_jci_handbook():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 30px 0; text-align: center;">
        <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.8rem; margin-bottom: 10px;">
            🏅 JCI Accreditation Standards
        </h1>
        <p style="color: #666; font-size: 1.1rem;">International Patient Safety Goals</p>
        <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #800020, #d4af37); 
             margin: 20px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/", 
                           height=750, scrolling=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# Feedback Form
def show_feedback():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 50px; margin-top: 30px;">
            <div style="text-align: center; margin-bottom: 40px;">
                <div style="font-size: 4rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">💬</div>
                <h2 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.5rem; 
                     margin-bottom: 10px;">Training Evaluation</h2>
                <p style="color: #666; font-size: 1.1rem;">Your feedback helps us improve the induction experience</p>
                <div style="width: 80px; height: 3px; background: linear-gradient(90deg, #800020, #d4af37); 
                     margin: 20px auto; border-radius: 2px;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("feedback_form"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                trainer_name = st.text_input("Trainer Name *", placeholder="Enter trainer name")
            with col_t2:
                training_topic = st.text_input("Training Topic *", placeholder="e.g., HR Admin Process")
            
            st.markdown("<h4 style='color: #800020; margin-top: 35px; margin-bottom: 25px; font-family: Playfair Display;'>Rate the Session (1-5 Scale)</h4>", 
                       unsafe_allow_html=True)
            
            ratings = {}
            parameters = [
                "Session sequence and flow",
                "Depth of content relevance", 
                "Usage of relevant methods",
                "Trainer engagement with participants",
                "Trainer readiness and knowledge",
                "Effective use of training methods",
                "Encouragement of participation",
                "Pace of training delivery",
                "Audibility and clarity",
                "Focus on learning outcomes"
            ]
            
            cols = st.columns(2)
            for idx, param in enumerate(parameters):
                with cols[idx % 2]:
                    ratings[param] = st.slider(param, 1, 5, 3, key=f"rate_{idx}")
            
            comments = st.text_area("Additional Comments (Optional)", height=120, 
                                   placeholder="Share your thoughts on how we can improve...")
            
            submitted = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
            
            if submitted:
                if trainer_name and training_topic:
                    avg_rating = sum(ratings.values()) / len(ratings)
                    feedback_data = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'user': st.session_state.user.get('name', 'Unknown'),
                        'email': st.session_state.user.get('email', 'Unknown'),
                        'trainer': trainer_name,
                        'topic': training_topic,
                        'average_rating': round(avg_rating, 2),
                        'comments': comments
                    }
                    save_feedback(feedback_data)
                    
                    st.success("🙏 Thank you for your valuable feedback! It helps us improve.")
                    time.sleep(2)
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in the trainer name and topic.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Passport/Report Card
def show_passport():
    st.markdown('<div class="main-container"></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 60px; margin: 40px auto; max-width: 900px; 
         background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(245,245,220,0.9) 100%); 
         border: 3px solid #d4af37; position: relative; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.15);">
        
        <!-- Decorative Elements -->
        <div style="position: absolute; top: -150px; right: -150px; width: 400px; height: 400px; 
             background: radial-gradient(circle, rgba(212,175,55,0.2) 0%, transparent 70%); 
             border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -100px; left: -100px; width: 300px; height: 300px; 
             background: radial-gradient(circle, rgba(128,0,32,0.1) 0%, transparent 70%); 
             border-radius: 50%;"></div>
        <div style="position: absolute; top: 30px; right: 30px; font-size: 5rem; opacity: 0.1;">🏥</div>
        
        <!-- Header -->
        <div style="text-align: center; border-bottom: 4px solid #800020; padding-bottom: 35px; margin-bottom: 45px; position: relative; z-index: 1;">
            <div style="font-size: 4rem; margin-bottom: 15px;">🛂</div>
            <h1 style="color: #800020; font-family: 'Playfair Display'; font-size: 2.8rem; margin-bottom: 10px;">
                Passport to Medanta
            </h1>
            <p style="color: #666; font-size: 1.2rem; letter-spacing: 4px; text-transform: uppercase; font-weight: 500;">
                Official Induction Certificate
            </p>
            <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #800020, #d4af37); 
                 margin: 20px auto 0; border-radius: 2px;"></div>
        </div>
        
        <!-- Employee Details Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 45px; position: relative; z-index: 1;">
            <div style="background: rgba(128,0,32,0.05); padding: 30px; border-radius: 18px; border-left: 4px solid #800020;">
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">Employee Name</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.5rem; font-family: 'Playfair Display';">{user.get('name', 'N/A')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 30px; border-radius: 18px; border-left: 4px solid #800020;">
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">Employee ID</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.5rem; font-family: 'Playfair Display';">{user.get('emp_id', 'Pending')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 30px; border-radius: 18px; border-left: 4px solid #800020;">
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">Department</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.5rem; font-family: 'Playfair Display';">{user.get('department', 'N/A')}</h3>
            </div>
            <div style="background: rgba(128,0,32,0.05); padding: 30px; border-radius: 18px; border-left: 4px solid #800020;">
                <p style="color: #888; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">Joining Date</p>
                <h3 style="color: #800020; margin: 0; font-size: 1.5rem; font-family: 'Playfair Display';">{datetime.now().strftime("%B %d, %Y")}</h3>
            </div>
        </div>
        
        <!-- Status Badge -->
        <div style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
             padding: 45px; border-radius: 25px; text-align: center; margin-bottom: 45px; position: relative; z-index: 1;
             box-shadow: 0 15px 50px rgba(128,0,32,0.3);">
            <p style="font-size: 1.1rem; margin-bottom: 15px; opacity: 0.9; letter-spacing: 3px; text-transform: uppercase;">
                Induction Status
            </p>
            <h2 style="font-size: 3rem; margin: 0; font-family: 'Playfair Display'; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
                ✅ COMPLETED
            </h2>
            <div style="width: 60px; height: 3px; background: rgba(255,255,255,0.5); margin: 20px auto; border-radius: 2px;"></div>
            <p style="margin: 0; opacity: 0.9; font-size: 1.05rem;">
                All modules successfully cleared with excellence
            </p>
        </div>
        
        <!-- Footer -->
        <div style="text-align: center; color: #666; font-size: 0.95rem; font-style: italic; position: relative; z-index: 1; line-height: 1.8;">
            <p style="margin-bottom: 20px;">This certifies that the above named employee has successfully completed<br>
            the mandatory induction program at <strong style="color: #800020;">Medanta - The Medicity</strong></p>
            
            <div style="background: rgba(212,175,55,0.1); padding: 20px; border-radius: 12px; margin-top: 25px; border: 1px solid rgba(212,175,55,0.3);">
                <p style="margin: 0; color: #800020; font-weight: 600; font-style: normal;">
                    Validated by: Learning & Development Department<br>
                    <span style="font-size: 0.9rem; color: #666; font-weight: 400;">
                        Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    </span>
                </p>
            </div>
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
