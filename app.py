import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Legalease - AI Legal Document Generator", layout="centered")

st.title("⚖️ Legalease: AI-Powered Legal Document Generator")
st.write("Simplify complex legal jargon into easy-to-understand terms.")

api_key = st.text_input("Enter your Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Upload a Legal Document (Text file)", type=["txt"])
user_prompt = st.text_area("Or Paste your Legal Text / Document here:")

if st.button("Simplify Legal Document"):
    if not api_key:
        st.error("Please provide a valid Gemini API key.")
    elif user_prompt:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Simplify this legal text into plain Tamil and simple English: {user_prompt}")
            st.subheader("Simplified Output:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please paste some legal text to analyze.")
