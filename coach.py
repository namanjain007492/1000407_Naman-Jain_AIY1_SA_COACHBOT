import streamlit as st
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CoachBot AI | NextGen Sports",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SECURE API KEY SETUP ---
try:
    # Fetches the key securely from .streamlit/secrets.toml or Streamlit Cloud Secrets
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except KeyError:
    st.error("⚠️ API Key missing! Please configure '.streamlit/secrets.toml' or Streamlit Cloud Secrets.")
    st.stop()

# --- HELPER FUNCTION: GEMINI API CALL ---
def get_ai_coach(prompt, temperature=0.7):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=1024,
            )
        )
        return response.text
    except Exception as e:
        return f"🚨 Generation Error: {str(e)}"

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
age = st.sidebar.number_input("Age", min_value=10, max_value=30, value=15)

st.sidebar.header("🩺 Health & Goals")
goal = st.sidebar.selectbox("Primary Goal", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength"])
injury_hist = st.sidebar.text_area("Injury History / Risk Zones", placeholder="e.g., Recovering from right knee strain")

st.sidebar.header("🥗 Nutrition")
diet = st.sidebar.selectbox("Dietary Preference", ["Standard (Non-Veg)", "Vegetarian", "Vegan"])
allergies = st.sidebar.text_input("Food Allergies", "None")

# --- MAIN DASHBOARD INTERFACE ---
st.subheader("🧠 Coaching Dashboard")

# Feature Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Workout Plan", "🩹 Recovery & Safety", "🎯 Tactics & Mindset", "🍎 Nutrition Plan"])

# 1. WORKOUT PLAN (Medium Temperature)
with tab1:
    st.markdown("### Personalized Warm-up & Workout Routine")
    intensity = st.select_slider("Select Training Intensity", options=["Light", "Moderate", "Vigorous"])
    
    if st.button("Generate Workout Plan"):
        if not position:
            st.warning("Please enter your position in the sidebar!")
        else:
            with st.spinner("CoachBot is designing your routine..."):
                prompt = f"""
                Create a {intensity} intensity, full-body workout plan and a personalized warm-up/cooldown 
                for a {age}-year-old {position} in {sport}. Goal: {goal}. 
                Ensure the exercises are age-appropriate.
                """
                # Temperature 0.5 for balanced, structured workout generation
                workout_plan = get_ai_coach(prompt, temperature=0.5)
                st.write(workout_plan)

# 2. RECOVERY & SAFETY (Low Temperature - Conservative/Accurate)
with tab2:
    st.markdown("### Injury Adaptation & Safe Training")
    if st.button("Generate Recovery Protocol"):
        if not injury_hist:
            st.info("No injuries reported. Keep up the good work! Add an injury in the sidebar to test this feature.")
        else:
            with st.spinner("Analyzing injury profile..."):
                prompt = f"""
                Act as a sports physiotherapist. Create a safe recovery training schedule and modifications 
                for a {sport} athlete dealing with: {injury_hist}. 
                Include what movements they MUST avoid to prevent further damage.
                """
                # Temperature 0.3 for highly accurate, conservative medical/safety advice
                recovery_plan = get_ai_coach(prompt, temperature=0.3)
                st.warning("⚠️ Always consult a medical professional before starting post-injury training.")
                st.write(recovery_plan)

# 3. TACTICS & MINDSET (High Temperature - Creative/Varied)
with tab3:
    st.markdown("### Tactical Advice & Mental Focus")
    skill = st.text_input("Specific skill you want to improve", placeholder="e.g., decision-making under pressure, bowling yorkers")
    
    if st.button("Get Tactical Tips"):
        with st.spinner("Drawing up the playbook..."):
            prompt = f"""
            Act as an elite {sport} coach. Provide creative, highly specific tactical coaching tips 
            to improve {skill} for a {position}. Include a pre-match visualization technique.
            """
            # Temperature 0.8 for creative tactical solutions and varied mental routines
            tactics = get_ai_coach(prompt, temperature=0.8)
            st.info(tactics)

# 4. NUTRITION PLAN (Data Visualization Integration)
with tab4:
    st.markdown("### Nutrition & Macro Guide")
    if st.button("Generate Meal Plan"):
        with st.spinner("Calculating macros..."):
            prompt = f"""
            Suggest a 1-day nutrition guide for a {age}-year-old {sport} athlete following a {diet} diet. 
            Allergies: {allergies}. Goal: {goal}. Keep it simple and structured.
            """
            # Temperature 0.6 for balanced meal suggestions
            nutrition = get_ai_coach(prompt, temperature=0.6)
            st.write(nutrition)
            
            # Interactive Visualization using Plotly & Pandas
            st.markdown("#### Suggested Daily Macronutrient Breakdown")
            
            # Simple logic to adjust macros based on user goal
            if goal == "Build Stamina":
                macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [55, 25, 20]}
            elif goal == "Strength":
                macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [40, 40, 20]}
            else:
                macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [45, 30, 25]}
                
            df = pd.DataFrame(macros)
            
            # Create interactive pie chart
            fig = px.pie(df, values='Percentage', names='Macronutrient', 
                         color='Macronutrient', 
                         color_discrete_map={'Carbohydrates':'#FF9999', 'Protein':'#66B2FF', 'Fats':'#99FF99'},
                         title=f"Target Macros for {goal}")
            st.plotly_chart(fig, use_container_width=True)
