import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CoachBot AI | NextGen Sports",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SECURE API KEY SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("⚠️ API Key missing! Please configure '.streamlit/secrets.toml' or Streamlit Cloud Secrets.")
    st.stop()

# --- HELPER FUNCTION: GEMINI API CALL (FREE TIER OPTIMIZED) ---
def get_ai_coach(prompt, temperature=0.7):
    try:
        # Using the official free-tier supported model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1024,
            )
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg and "limit: 0" in error_msg:
            return "🚨 **QUOTA ERROR:** Google has blocked your free tier (Limit 0). To fix this, you MUST go to Google Cloud Console, select your API project, and enable a Billing Account to unlock your 1,500 free daily requests."
        return f"🚨 Generation Error: {error_msg}"

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; background-color: #004D40; color: white; }
    .stButton>button:hover { background-color: #00251A; color: white; }
    .header-text { font-size: 2.2rem; font-weight: 800; color: #1E1E1E; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="header-text">🏃 CoachBot AI</p>', unsafe_allow_html=True)
st.markdown("Virtual assistant providing personalized, injury-safe sports training and tactical coaching.")
st.divider()

# --- SIDEBAR: ATHLETE PROFILE INPUTS ---
st.sidebar.header("👤 Athlete Profile")
sport = st.sidebar.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
position = st.sidebar.text_input("Player Position", placeholder="e.g., Striker, Fast Bowler, Point Guard")
age = st.sidebar.number_input("Age", min_value=8, max_value=30, value=15)

st.sidebar.header("🩺 Health & Goals")
goal = st.sidebar.selectbox("Primary Goal", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength"])
injury_hist = st.sidebar.text_area("Injury History / Risk Zones", placeholder="e.g., Recovering from right knee strain")

st.sidebar.header("🥗 Nutrition")
diet = st.sidebar.selectbox("Dietary Preference", ["Standard (Non-Veg)", "Vegetarian", "Vegan"])
allergies = st.sidebar.text_input("Food Allergies", "None")

# --- MAIN DASHBOARD INTERFACE ---
st.subheader("🧠 Coaching Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Workout Plan", "🩹 Recovery & Safety", "🎯 Tactics & Mindset", "🍎 Nutrition Plan"])

with tab1:
    st.markdown("### Personalized Warm-up & Workout Routine")
    intensity = st.select_slider("Select Training Intensity", options=["Light", "Moderate", "Vigorous"])
    if st.button("Generate Workout Plan"):
        if not position:
            st.warning("Please enter your position in the sidebar to get a personalized plan!")
        else:
            with st.spinner("CoachBot is designing your routine..."):
                prompt = f"Create a {intensity} intensity, full-body workout plan and warm-up for a {age}-year-old {position} in {sport}. Goal: {goal}."
                st.write(get_ai_coach(prompt, temperature=0.5))

with tab2:
    st.markdown("### Injury Adaptation & Safe Training")
    if st.button("Generate Recovery Protocol"):
        if not injury_hist:
            st.info("No injuries reported. Keep up the good work!")
        else:
            with st.spinner("Analyzing injury profile..."):
                prompt = f"Act as a sports physiotherapist. Create a safe recovery schedule for a {sport} athlete dealing with: {injury_hist}. Include movements they MUST avoid."
                st.warning("⚠️ Always consult a medical professional before starting post-injury training.")
                st.write(get_ai_coach(prompt, temperature=0.3))

with tab3:
    st.markdown("### Tactical Advice & Mental Focus")
    skill = st.text_input("Specific skill you want to improve", placeholder="e.g., decision-making under pressure")
    if st.button("Get Tactical Tips"):
        with st.spinner("Drawing up the playbook..."):
            prompt = f"Act as an elite {sport} coach. Provide specific tactical coaching tips to improve '{skill}' for a {position}. Include a pre-match visualization technique."
            st.info(get_ai_coach(prompt, temperature=0.8))

with tab4:
    st.markdown("### Nutrition & Macro Guide")
    if st.button("Generate Meal Plan"):
        with st.spinner("Calculating macros..."):
            prompt = f"Suggest a 1-day nutrition guide for a {age}-year-old {sport} athlete on a {diet} diet. Allergies: {allergies}. Goal: {goal}."
            st.write(get_ai_coach(prompt, temperature=0.6))
            
            st.markdown("#### Suggested Daily Macronutrient Breakdown")
            macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [55, 25, 20]} if goal == "Build Stamina" else {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [40, 40, 20]} if goal == "Strength" else {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [45, 30, 25]}
            df = pd.DataFrame(macros)
            fig = px.pie(df, values='Percentage', names='Macronutrient', color='Macronutrient', color_discrete_map={'Carbohydrates':'#FF9999', 'Protein':'#66B2FF', 'Fats':'#99FF99'})
            st.plotly_chart(fig, use_container_width=True)
