import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CoachBot AI | Pro Edition",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API SETUP ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ API Key missing! Please configure '.streamlit/secrets.toml'.")
    st.stop()

# --- AI HELPER: TEXT GENERATOR ---
def get_ai_text(prompt, temperature=0.7):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        ).text
    except Exception as e:
        return f"🚨 Generation Error: {str(e)}"

# --- AI HELPER: STRUCTURED JSON DATA GENERATOR ---
def get_ai_data(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, # Low temp keeps data formatting highly strict
                response_mime_type="application/json" 
            )
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Data parsing failed: {e}")
        return None

# --- UI STYLING ---
st.markdown("""
    <style>
    .stButton>button { border-radius: 6px; font-weight: bold; width: 100%; background-color: #1E3A8A; color: white; transition: 0.2s; }
    .stButton>button:hover { background-color: #172554; border-color: #172554; color: white; transform: scale(1.01); }
    .main-title { font-size: 2.5rem; font-weight: 900; color: #0F172A; margin-bottom: 0px;}
    .sub-title { font-size: 1.1rem; color: #475569; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🏅 CoachBot AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">NextGen Sports Lab: Advanced Training & Data Dashboard</p>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR: ATHLETE PROFILE ---
with st.sidebar:
    st.header("👤 Athlete Profile")
    sport = st.selectbox("Sport Focus", ["Football", "Cricket", "Basketball", "Athletics", "Tennis"])
    position = st.text_input("Player Position", placeholder="e.g., Center Back, Fast Bowler")
    age = st.slider("Age", min_value=10, max_value=35, value=16)

    st.header("🩺 Health & Goals")
    goal = st.selectbox("Primary Goal", ["Build Stamina", "Explosive Strength", "Post-Injury Recovery", "Tactical IQ"])
    injury_hist = st.text_area("Injury History", placeholder="e.g., Left ankle sprain (2 months ago)")

    st.header("🥗 Nutrition Profile")
    diet = st.selectbox("Dietary Preference", ["Standard (Non-Veg)", "Vegetarian", "Vegan", "High-Protein"])
    allergies = st.text_input("Allergies / Restrictions", "None")

# --- MAIN DASHBOARD ---
tab1, tab2, tab3, tab4 = st.tabs(["🏋️‍♂️ 7-Day Protocol", "🩹 Rehab & Safety", "🎯 Tactical Playbook", "🍎 Macro Data"])

# 1. TABULAR WORKOUT DATA
with tab1:
    st.subheader("Structured Weekly Training Data")
    intensity = st.select_slider("Target Intensity", options=["Light Recovery", "Moderate", "High Performance"])
    
    if st.button("Generate Training Database"):
        if not position:
            st.warning("Please define your position in the sidebar first.")
        else:
            with st.spinner("Compiling structured workout metrics..."):
                prompt = f"""
                Create a 7-day, {intensity} intensity workout plan for a {age}yo {position} in {sport}. Goal: {goal}.
                Return ONLY a JSON array containing 7 objects.
                Keys must be exactly: "Day", "Focus_Area", "Primary_Exercise", "Sets_and_Reps", "Duration_Mins".
                """
                data = get_ai_data(prompt)
                if data:
                    df = pd.DataFrame(data)
                    # Styling the Pandas DataFrame for a premium look
                    st.dataframe(df.style.set_properties(**{'background-color': '#f8fafc', 'color': '#0f172a', 'border-color': '#e2e8f0'}), use_container_width=True, hide_index=True)
                else:
                    st.error("Data generation encountered an issue. Please try again.")

# 2. RECOVERY TEXT
with tab2:
    st.subheader("Injury Adaptation Protocol")
    if st.button("Generate Rehab Strategy"):
        if not injury_hist:
            st.info("No active injuries reported. Add an injury in the sidebar to generate a protocol.")
        else:
            with st.spinner("Analyzing biomechanical data..."):
                prompt = f"Act as an elite sports physiotherapist. Detail a phase-by-phase safe recovery schedule for a {sport} athlete dealing with: {injury_hist}. Emphasize 3 specific movements they MUST avoid."
                st.warning("⚠️ Medical Disclaimer: Always consult a certified physical therapist before beginning post-injury training.")
                st.write(get_ai_text(prompt, temperature=0.3))

# 3. TACTICS TEXT
with tab3:
    st.subheader("Situational Tactics & Mindset")
    skill = st.text_input("Target Skill", placeholder="e.g., High-pressure passing, bowling yorkers in the death overs")
    if st.button("Generate Playbook"):
        if not skill:
            st.warning("Enter a specific skill to improve.")
        else:
            with st.spinner("Consulting the playbook..."):
                prompt = f"Act as a professional {sport} head coach. Provide 3 advanced tactical tips to master '{skill}' for a {position}. Follow it with a 1-minute pre-match visualization script."
                st.info(get_ai_text(prompt, temperature=0.8))

# 4. TABULAR NUTRITION DATA & VISUALIZATION
with tab4:
    st.subheader("Nutritional Data & Macro Visualization")
    if st.button("Generate Diet Database"):
        with st.spinner("Calculating caloric load and macros..."):
            prompt = f"""
            Design a 1-day high-performance meal plan for a {sport} athlete on a {diet} diet. Allergies: {allergies}. Goal: {goal}.
            Return ONLY a JSON array of objects representing meals (Breakfast, Lunch, Snack, Dinner).
            Keys must be exactly: "Meal_Time", "Food_Item", "Portion_Size", "Calories", "Protein_g", "Carbs_g", "Fats_g".
            """
            data = get_ai_data(prompt)
            if data:
                # 1. Render Table
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # 2. Render Chart
                st.markdown("#### Target Macronutrient Distribution")
                
                # Dynamic macro adjustment based on goal
                if goal == "Build Stamina":
                    macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [55, 25, 20]}
                elif goal == "Explosive Strength":
                    macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [40, 40, 20]}
                else:
                    macros = {"Macronutrient": ["Carbohydrates", "Protein", "Fats"], "Percentage": [45, 30, 25]}
                
                macro_df = pd.DataFrame(macros)
                fig = px.pie(
                    macro_df, 
                    values='Percentage', 
                    names='Macronutrient', 
                    color='Macronutrient', 
                    color_discrete_map={'Carbohydrates':'#38bdf8', 'Protein':'#fb7185', 'Fats':'#facc15'},
                    hole=0.4 # Turns pie chart into a modern donut chart
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
