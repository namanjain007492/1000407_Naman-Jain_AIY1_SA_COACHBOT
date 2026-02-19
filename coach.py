# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

st.set_page_config(
    page_title="CoachBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API Key missing. Configure '.streamlit/secrets.toml'.")
    st.stop()

def get_ai_text(prompt, temperature=0.7):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        ).text
    except Exception as e:
        return f"Generation Error: {str(e)}"

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

st.markdown("""
    <style>
    .stButton>button { border-radius: 8px; font-weight: bold; width: 100%; background-color: #004D40; color: white; }
    .stButton>button:hover { background-color: #00251A; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏃 CoachBot AI")
st.markdown("Virtual assistant providing personalized sports training and tactical coaching.")
st.divider()

st.sidebar.header("👤 Athlete Profile")
sport = st.sidebar.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
position = st.sidebar.text_input("Position", placeholder="e.g., Striker, Fast Bowler")
age = st.sidebar.number_input("Age", min_value=8, max_value=30, value=15)

st.sidebar.header("🩺 Health & Goals")
goal = st.sidebar.selectbox("Goal", ["Build Stamina", "Post-Injury Recovery", "Tactical Improvement", "Strength"])
injury_hist = st.sidebar.text_area("Injury History", placeholder="e.g., Right knee strain")

st.sidebar.header("🥗 Nutrition")
diet = st.sidebar.selectbox("Diet", ["Standard", "Vegetarian", "Vegan"])
allergies = st.sidebar.text_input("Allergies", "None")

tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ Weekly Plan", "🩹 Recovery", "🎯 Tactics", "🍎 Nutrition Data"])

with tab1:
    intensity = st.select_slider("Training Intensity", options=["Light", "Moderate", "Vigorous"])
    if st.button("Generate Training Table"):
        if not position:
            st.warning("Please enter your position.")
        else:
            with st.spinner("Compiling structured tabular data..."):
                prompt = f"""
                Create a 7-day, {intensity} intensity workout plan for a {age}yo {position} in {sport}. Goal: {goal}.
                Return ONLY a JSON array of 7 objects.
                Keys exactly: "Day", "Focus", "Exercises", "Duration_Mins".
                """
                data = get_ai_data(prompt)
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                else:
                    st.error("Data formatting failed. Retry.")

with tab2:
    if st.button("Generate Recovery Protocol"):
        if not injury_hist:
            st.info("No injuries reported.")
        else:
            with st.spinner("Analyzing injury..."):
                prompt = f"Act as a physiotherapist. Create a safe recovery schedule for a {sport} athlete with: {injury_hist}. Include movements to avoid."
                st.write(get_ai_text(prompt, temperature=0.3))

with tab3:
    skill = st.text_input("Skill to improve", placeholder="e.g., decision-making")
    if st.button("Get Tactical Tips"):
        with st.spinner("Generating plays..."):
            prompt = f"Act as an elite {sport} coach. Provide specific tactical tips to improve '{skill}' for a {position}. Include a visualization technique."
            st.info(get_ai_text(prompt, temperature=0.8))

with tab4:
    if st.button("Generate Diet Table"):
        with st.spinner("Calculating macros..."):
            prompt = f"""
            Suggest a 1-day meal plan for a {sport} athlete on a {diet} diet. Allergies: {allergies}. Goal: {goal}.
            Return ONLY a JSON array of objects representing meals.
            Keys exactly: "Meal", "Food_Item", "Calories", "Protein_g", "Carbs_g", "Fats_g".
            """
            data = get_ai_data(prompt)
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                
                macros = {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [55, 25, 20]} if goal == "Build Stamina" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [40, 40, 20]} if goal == "Strength" else {"Macronutrient": ["Carbs", "Protein", "Fats"], "Percentage": [45, 30, 25]}
                fig = px.pie(pd.DataFrame(macros), values='Percentage', names='Macronutrient', color='Macronutrient', color_discrete_map={'Carbs':'#FF9999', 'Protein':'#66B2FF', 'Fats':'#99FF99'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Data formatting failed. Retry.")
