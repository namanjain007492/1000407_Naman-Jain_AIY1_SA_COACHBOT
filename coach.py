import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CoachBot AI | Pro", page_icon="🏅", layout="wide")

# --- SECURE API SETUP ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API Key missing! Configure '.streamlit/secrets.toml'.")
    st.stop()

# --- AI HELPER: HYBRID DATA GENERATOR (TEXT + TABLE) ---
def get_hybrid_ai_data(prompt):
    """Forces Gemini to return a JSON object containing BOTH a text brief and a data array."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, 
                response_mime_type="application/json" 
            )
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Data Generation Error: {str(e)}")
        return None

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 6px; font-weight: bold; width: 100%; background-color: #1E3A8A; color: white; }
    .stButton>button:hover { background-color: #172554; color: white; }
    .brief-text { font-size: 1.1rem; color: #334155; border-left: 4px solid #1E3A8A; padding-left: 15px; margin-bottom: 20px; background-color: #F8FAFC; padding-top: 10px; padding-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏃 CoachBot AI: Hybrid Data Dashboard")
st.divider()

# --- SIDEBAR: ATHLETE PROFILE ---
with st.sidebar:
    st.header("👤 Athlete Profile")
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
    position = st.text_input("Position", placeholder="e.g., Striker, Point Guard")
    age = st.slider("Age", 8, 35, 16)

    st.header("🩺 Health & Goals")
    goal = st.selectbox("Goal", ["Build Stamina", "Explosive Strength", "Post-Injury Recovery", "Tactical IQ"])
    injury_hist = st.text_area("Injury History", placeholder="e.g., Left ankle sprain")

    st.header("🥗 Nutrition")
    diet = st.selectbox("Diet", ["Standard", "Vegetarian", "Vegan", "High-Protein"])
    allergies = st.text_input("Allergies", "None")

# --- MAIN DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Weekly Protocol", "🩹 Rehab Strategy", "🎯 Tactical Drills", "🍎 Diet Metrics"])

# 1. HYBRID WORKOUT DATA
with tab1:
    intensity = st.select_slider("Target Intensity", options=["Light", "Moderate", "High"])
    if st.button("Generate Detailed Workout"):
        if not position:
            st.warning("Please define your position in the sidebar.")
        else:
            with st.spinner("Processing hybrid workout data..."):
                prompt = f"""
                Create a 7-day, {intensity} intensity workout plan for a {age}yo {position} in {sport}. Goal: {goal}.
                Return a JSON object with exactly TWO keys:
                1. "coach_brief": A 3-sentence summary of the week's training philosophy.
                2. "workout_table": A JSON array of 7 objects with keys: "Day", "Focus", "Primary_Exercises", "Sets_x_Reps", "Rest_Time".
                """
                data = get_hybrid_ai_data(prompt)
                if data:
                    st.markdown(f'<div class="brief-text"><strong>Coach\'s Summary:</strong><br>{data.get("coach_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("workout_table", [])), use_container_width=True, hide_index=True)

# 2. HYBRID RECOVERY DATA
with tab2:
    if st.button("Generate Rehab Protocol"):
        if not injury_hist:
            st.info("No active injuries reported.")
        else:
            with st.spinner("Analyzing biomechanics..."):
                prompt = f"""
                Create a rehab protocol for a {sport} athlete with: {injury_hist}.
                Return a JSON object with exactly TWO keys:
                1. "medical_brief": A 3-sentence summary of the injury and the primary healing mechanism.
                2. "rehab_table": A JSON array of 4 objects representing recovery phases. Keys: "Phase", "Duration", "Safe_Mobility_Drills", "Movements_To_Strictly_Avoid".
                """
                data = get_hybrid_ai_data(prompt)
                if data:
                    st.markdown(f'<div class="brief-text"><strong>Medical Assessment:</strong><br>{data.get("medical_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("rehab_table", [])), use_container_width=True, hide_index=True)

# 3. HYBRID TACTICAL DATA
with tab3:
    skill = st.text_input("Target Skill", placeholder="e.g., High-pressure passing")
    if st.button("Generate Tactical Playbook"):
        if not skill:
            st.warning("Enter a skill to improve.")
        else:
            with st.spinner("Compiling playbook..."):
                prompt = f"""
                Provide a tactical breakdown to master '{skill}' for a {position} in {sport}.
                Return a JSON object with exactly TWO keys:
                1. "tactical_brief": A 3-sentence mindset and situational awareness summary.
                2. "drill_table": A JSON array of 3 specific practice drills. Keys: "Drill_Name", "Execution_Steps", "Key_Focus_Area", "Duration_Mins".
                """
                data = get_hybrid_ai_data(prompt)
                if data:
                    st.markdown(f'<div class="brief-text"><strong>Mindset & Strategy:</strong><br>{data.get("tactical_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("drill_table", [])), use_container_width=True, hide_index=True)

# 4. HYBRID NUTRITION DATA & CHARTS
with tab4:
    if st.button("Generate Diet Metrics"):
        with st.spinner("Calculating macros..."):
            prompt = f"""
            Design a 1-day meal plan for a {sport} athlete. Diet: {diet}. Allergies: {allergies}. Goal: {goal}.
            Return a JSON object with exactly TWO keys:
            1. "nutrition_brief": A 3-sentence summary explaining how this specific food fuels their specific goal.
            2. "meal_table": A JSON array of 4 objects. Keys: "Meal", "Dish", "Ingredients", "Calories", "Protein_g", "Carbs_g", "Fats_g".
            """
            data = get_hybrid_ai_data(prompt)
            if data:
                st.markdown(f'<div class="brief-text"><strong>Nutrition Strategy:</strong><br>{data.get("nutrition_brief", "")}</div>', unsafe_allow_html=True)
                
                df = pd.DataFrame(data.get("meal_table", []))
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Render Target Macros Chart
                st.markdown("#### Macro Distribution Targets")
                macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [55, 25, 20]} if goal == "Build Stamina" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [40, 40, 20]} if goal == "Explosive Strength" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [45, 30, 25]}
                fig = px.pie(pd.DataFrame(macros), values='Percentage', names='Macronutrient', color='Macronutrient', color_discrete_map={'Carbs':'#38bdf8', 'Protein':'#fb7185', 'Fats':'#facc15'}, hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
