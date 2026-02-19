import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CoachBot AI | Elite Level", page_icon="🏆", layout="wide")

# --- SECURE API SETUP ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API Key missing! Configure '.streamlit/secrets.toml'.")
    st.stop()

# --- AI HELPER: ULTRA-DETAILED JSON GENERATOR ---
def get_detailed_ai_data(prompt):
    """Forces Gemini to return a highly complex JSON object for deep tabular rendering."""
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
    .stButton>button { border-radius: 6px; font-weight: bold; width: 100%; background-color: #0F172A; color: white; padding: 10px;}
    .stButton>button:hover { background-color: #334155; color: white; }
    .brief-text { font-size: 1.15rem; color: #1E293B; border-left: 5px solid #2563EB; padding: 15px; margin-bottom: 25px; background-color: #F8FAFC; border-radius: 0px 8px 8px 0px; line-height: 1.6;}
    .metric-label { font-weight: 800; color: #2563EB; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 CoachBot AI: Elite Sports Science Dashboard")
st.markdown("Advanced biomechanical, tactical, and metabolic data mapping for next-generation athletes.")
st.divider()

# --- SIDEBAR: DEEP ATHLETE PROFILE ---
with st.sidebar:
    st.header("👤 Athlete Biometrics")
    sport = st.selectbox("Sport Focus", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
    position = st.text_input("Positional Role", placeholder="e.g., Box-to-Box Midfielder")
    age = st.slider("Age", 10, 35, 18)
    weight_kg = st.number_input("Weight (kg)", 40, 120, 65)

    st.header("🩺 Medical & Goals")
    goal = st.selectbox("Macrocycle Goal", ["Hypertrophy & Strength", "Aerobic Stamina", "Speed & Agility", "Post-Op Rehab"])
    injury_hist = st.text_area("Clinical Injury History", placeholder="e.g., Grade 2 Hamstring Tear (3 months ago)")

    st.header("🥗 Metabolic Profile")
    diet = st.selectbox("Dietary Protocol", ["Standard Macro", "Vegetarian", "Vegan", "Keto/Low-Carb"])
    allergies = st.text_input("Known Allergies", "None")

# --- MAIN DASHBOARD TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Microcycle (7-Day Plan)", "🩹 Biomechanical Rehab", "🎯 Tactical Blueprint", "🍎 Metabolic Data"])

# 1. ULTRA-DETAILED WORKOUT DATA
with tab1:
    st.subheader("7-Day Training Microcycle")
    intensity = st.select_slider("Target Load (RPE)", options=["Light (RPE 4-5)", "Moderate (RPE 6-7)", "Maximal (RPE 8-10)"])
    
    if st.button("Generate Microcycle Data"):
        if not position:
            st.warning("Please define your positional role in the sidebar.")
        else:
            with st.spinner("Compiling physiological load data..."):
                prompt = f"""
                Create a highly detailed 7-day, {intensity} intensity workout plan for an {age}yo, {weight_kg}kg {position} in {sport}. Goal: {goal}.
                Return a JSON object with exactly TWO keys:
                1. "coach_brief": A 4-sentence summary of the physiological adaptations targeted this week.
                2. "workout_table": A JSON array of 7 objects. Keys MUST be: "Day", "Phase" (e.g., Warmup, Main, Finisher), "Exercise_Name", "Sets", "Reps_or_Time", "Target_RPE", "Rest_Seconds", "Biomechanical_Cue".
                """
                data = get_detailed_ai_data(prompt)
                if data:
                    st.markdown(f'<div class="brief-text"><span class="metric-label">Physiology Brief:</span><br>{data.get("coach_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("workout_table", [])), use_container_width=True, hide_index=True)

# 2. ULTRA-DETAILED REHAB DATA
with tab2:
    st.subheader("Clinical Rehabilitation Protocol")
    if st.button("Generate Clinical Rehab Protocol"):
        if not injury_hist:
            st.info("No clinical injuries reported. Enter data in the sidebar to generate a protocol.")
        else:
            with st.spinner("Analyzing anatomical restrictions..."):
                prompt = f"""
                Create a clinical rehab protocol for a {sport} athlete with: {injury_hist}.
                Return a JSON object with exactly TWO keys:
                1. "medical_brief": A 4-sentence anatomical explanation of the tissue damage and the cellular healing mechanism required.
                2. "rehab_table": A JSON array of 4 phases (Acute, Sub-Acute, Remodeling, Return-to-Play). Keys MUST be: "Phase_Name", "Estimated_Timeline", "Primary_Clinical_Goal", "Approved_Kinesiology_Drills", "Strict_Contraindications", "Pain_Scale_Limit_Out_Of_10".
                """
                data = get_detailed_ai_data(prompt)
                if data:
                    
                    st.markdown(f'<div class="brief-text"><span class="metric-label">Anatomical Assessment:</span><br>{data.get("medical_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("rehab_table", [])), use_container_width=True, hide_index=True)

# 3. ULTRA-DETAILED TACTICAL DATA
with tab3:
    st.subheader("Positional Tactical Blueprint")
    skill = st.text_input("Target Skill/Phase", placeholder="e.g., Transitioning from defense to attack, Bowling Death Overs")
    if st.button("Generate Tactical Blueprint"):
        if not skill:
            st.warning("Enter a specific skill phase to improve.")
        else:
            with st.spinner("Rendering situational playbook..."):
                prompt = f"""
                Provide an elite tactical breakdown to master '{skill}' for a {position} in {sport}.
                Return a JSON object with exactly TWO keys:
                1. "tactical_brief": A 4-sentence overview of the spatial awareness and decision-making required for this skill.
                2. "drill_table": A JSON array of 4 specific field drills. Keys MUST be: "Drill_Name", "Field_Setup", "Execution_Mechanics", "Key_Visual_Cues", "Success_Metric", "Duration_Mins".
                """
                data = get_detailed_ai_data(prompt)
                if data:
                    
                    st.markdown(f'<div class="brief-text"><span class="metric-label">Spatial & Cognitive Strategy:</span><br>{data.get("tactical_brief", "")}</div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(data.get("drill_table", [])), use_container_width=True, hide_index=True)

# 4. ULTRA-DETAILED NUTRITION DATA
with tab4:
    st.subheader("Metabolic & Hydration Schedule")
    if st.button("Generate Metabolic Data"):
        with st.spinner("Calculating basal metabolic rate and active load macros..."):
            prompt = f"""
            Design a highly specific 1-day metabolic meal plan for an {age}yo, {weight_kg}kg {sport} athlete. Diet: {diet}. Allergies: {allergies}. Goal: {goal}.
            Return a JSON object with exactly TWO keys:
            1. "nutrition_brief": A 4-sentence summary explaining the glycemic index choices, protein synthesis timing, and hydration strategy.
            2. "meal_table": A JSON array of 5 exact timings (e.g., Pre-Workout, Breakfast, Post-Workout, Lunch, Dinner). Keys MUST be: "Timing_Window", "Meal_Type", "Exact_Food_Items", "Precise_Portions", "Total_Kcals", "Protein_g", "Carbs_g", "Fats_g", "Hydration_Target_ml".
            """
            data = get_detailed_ai_data(prompt)
            if data:
                
                st.markdown(f'<div class="brief-text"><span class="metric-label">Metabolic Strategy:</span><br>{data.get("nutrition_brief", "")}</div>', unsafe_allow_html=True)
                
                df = pd.DataFrame(data.get("meal_table", []))
                # Highlighting numeric columns for better readability
                st.dataframe(df.style.format(precision=0, subset=["Total_Kcals", "Protein_g", "Carbs_g", "Fats_g", "Hydration_Target_ml"]), use_container_width=True, hide_index=True)
                
                # Render Target Macros Chart based on Dynamic Goal
                st.markdown("#### Prescribed Macronutrient Ratio")
                if goal in ["Hypertrophy & Strength", "Post-Op Rehab"]:
                    macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [40, 35, 25]}
                elif goal == "Aerobic Stamina":
                    macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [60, 20, 20]}
                else:
                    macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [50, 25, 25]}
                    
                fig = px.pie(pd.DataFrame(macros), values='Percentage', names='Macronutrient', color='Macronutrient', color_discrete_map={'Carbs':'#38bdf8', 'Protein':'#fb7185', 'Fats':'#facc15'}, hole=0.45)
                fig.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+percent', textfont_size=14)
                st.plotly_chart(fig, use_container_width=True)
