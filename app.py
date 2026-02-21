import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -----------------------------
# Load API key and create client
# -----------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# -----------------------------
# Streamlit page configuration
# -----------------------------
st.set_page_config(
    page_title="Doctor Bot",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar for options
# -----------------------------
st.sidebar.title("Settings")
severity = st.sidebar.slider(
    "Severity of symptoms:",
    min_value=1,
    max_value=10,
    value=5,
    help="Select how severe your symptoms are from 1 (mild) to 10 (severe)"
)

st.sidebar.markdown("---")
st.sidebar.write("This is an AI-based doctor bot. ⚠️ Not real medical advice.")

# -----------------------------
# Main title and instructions
# -----------------------------
st.title("🩺 AI Doctor Bot")
st.markdown(
    "Describe your symptoms below and get AI-generated advice. "
    "Please note this is **educational only**."
)

# -----------------------------
# User input
# -----------------------------
symptoms = st.text_area("Enter your symptoms:", height=150)


# -----------------------------
# Get advice button
# -----------------------------
if st.button("Get Advice"):
    if not symptoms.strip():
        st.warning("Please enter your symptoms before getting advice.")
    else:
        prompt = f"""
You are a helpful medical assistant.
Patient symptoms: {symptoms}
Severity level: {severity}

Provide:
1. Possible causes
2. Precautions
3. When to see a doctor
Keep your explanation simple and easy to understand.
        """
        # Show loading spinner while generating
        with st.spinner("Consulting the AI doctor... 🩺"):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                advice = response.text
            except Exception as e:
                advice = f"❌ Error: {e}"

        # -----------------------------
        # Display AI response nicely
        # -----------------------------
        st.markdown("### Doctor's Advice:")
        st.markdown(f"<div style='background-color:#f0f2f6;padding:15px;border-radius:10px'>{advice}</div>", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<small> | Educational purposes only ⚠️</small>",
    unsafe_allow_html=True
)


