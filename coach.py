import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

st.set_page_config(page_title="CoachBot AI", page_icon="🏅", layout="wide")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API Key missing! Configure '.streamlit/secrets.toml'.")
    st.stop()

def get_ai_text(prompt, temperature=0.7):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        ).text
    except Exception as e:
        return f"Error: {str(e)}"

def get_ai_data(prompt):
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
        return None

st.title("🏃 CoachBot AI: Elite Training Dashboard")
st.divider()

with st.sidebar:
    st.header("👤 Athlete Profile")
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
    position = st.text_input("Position", placeholder="e.g., Center Back, Bowler")
    age = st.slider("Age", 8, 35, 16)

    st.header("🩺 Health & Goals")
    goal = st.selectbox("Goal", ["Build Stamina", "Explosive Strength", "Post-Injury Recovery", "Tactical IQ"])
    injury_hist = st.text_area("Injury History", placeholder="e.g., Left ankle sprain")

    st.header("🥗 Nutrition Profile")
    diet = st.selectbox("Diet", ["Standard", "Vegetarian", "Vegan", "High-Protein"])
    allergies = st.text_input("Allergies", "None")

tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ 7-Day Protocol", "🩹 Rehab & Safety", "🎯 Tactical Playbook", "🍎 Macro Data"])

with tab1:
    intensity = st.select_slider("Target Intensity", options=["Light Recovery", "Moderate", "High Performance"])
    if st.button("Generate Detailed Training Database"):
        if not position:
            st.warning("Please define your position in the sidebar.")
        else:
            with st.spinner("Compiling detailed workout metrics..."):
                prompt = f"""
                Create a detailed 7-day, {intensity} intensity workout plan for a {age}yo {position} in {sport}. Goal: {goal}.
                Return ONLY a JSON array containing 7 objects.
                Keys must be exactly: "Day", "Focus_Area", "Detailed_Routine", "Sets_and_Reps", "Rest_Periods", "Duration_Mins".
                """
                data = get_ai_data(prompt)
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                else:
                    st.error("Data generation failed. Please try again.")

with tab2:
    if st.button("Generate Detailed Rehab Strategy"):
        if not injury_hist:
            st.info("No active injuries reported.")
        else:
            with st.spinner("Analyzing biomechanics..."):
                prompt = f"Act as an elite physiotherapist. Detail a comprehensive, phase-by-phase recovery schedule for a {sport} athlete with: {injury_hist}. Emphasize exact biomechanical movements they MUST avoid and specific mobility drills to perform."
                st.warning("⚠️ Always consult a physical therapist before post-injury training.")
                st.write(get_ai_text(prompt, temperature=0.3))

with tab3:
    skill = st.text_input("Target Skill", placeholder="e.g., High-pressure passing")
    if st.button("Generate Elite Playbook"):
        if not skill:
            st.warning("Enter a specific skill to improve.")
        else:
            with st.spinner("Consulting the playbook..."):
                prompt = f"Act as a professional {sport} coach. Provide a detailed, 3-step tactical breakdown to master '{skill}' for a {position}. Include situational awareness cues and a pre-match visualization script."
                st.info(get_ai_text(prompt, temperature=0.8))

with tab4:
    if st.button("Generate Detailed Diet Database"):
        with st.spinner("Calculating precision macros..."):
            prompt = f"""
            Design a highly detailed 1-day meal plan for a {sport} athlete on a {diet} diet. Allergies: {allergies}. Goal: {goal}.
            Return ONLY a JSON array of objects representing 4 meals (Breakfast, Lunch, Snack, Dinner).
            Keys must be exactly: "Meal", "Dish_Name", "Exact_Ingredients", "Calories", "Protein_g", "Carbs_g", "Fats_g".
            """
            data = get_ai_data(prompt)
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                
                macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [55, 25, 20]} if goal == "Build Stamina" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [40, 40, 20]} if goal == "Explosive Strength" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [45, 30, 25]}
                fig = px.pie(pd.DataFrame(macros), values='Percentage', names='Macronutrient', color='Macronutrient', color_discrete_map={'Carbs':'#38bdf8', 'Protein':'#fb7185', 'Fats':'#facc15'}, hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Data generation failed. Please try again.")
