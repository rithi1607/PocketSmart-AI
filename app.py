import streamlit as st
from google import genai
import os

# Gemini Client - Epic 1
client = genai.Client(api_key="AQ.Ab8RN6LtdFiSKvke1jkL5h1_yRQY-ek1oyaTZ_migoaRmM7Pfg")

st.set_page_config(page_title="PocketSmart AI", page_icon="💰")
st.title("💰 PocketSmart AI: Your Smart Budget & Recommendation Assistant")

st.write("Welcome to PocketSmart AI - Built with Gemini 1.5 Flash")

# Epic 1 - Basic Gemini Test
if st.button("Test Gemini Connection"):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Give me 3 budget tips for students in Chennai"
    )
    st.success(response.text)
