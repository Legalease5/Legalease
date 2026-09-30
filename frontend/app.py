import sys
import os

# Root directory path-ஐ Python search path-ல் சேர்க்கிறது
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
from ai_core.generator import format_docx, format_pdf, format_html_preview, sanitize_text

# Page Configuration
st.set_page_config(page_title="LegalEase", layout="centered")

# Header section with Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("Image/Logo.png"):
        st.image("Image/Logo.png", use_container_width=True)

st.markdown("<h2 style='text-align: center;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)
st.write("Fill in the details below to generate a tailored legal document.")

# Input Form Fields
doc_type = st.text_input("Document Type (e.g. Agreement, Contract, NDA)", "Work Contract")
parties = st.text_area("Parties Involved", "John Doe (Service Provider), TechNova Inc. (Client)")
key_terms = st.text_area("Key Terms & Conditions (Use semicolons for bullet points)", "Deliverables must be completed by target date; Payment within 7 days")
effective_date = st.text_input("Effective Date", "October 1, 2026")

# Generate Document Button
if st.button("Generate Document"):
    if not doc_type or not parties or not key_terms or not effective_date:
        st.warning("Please fill in all fields before generating.")
    else:
        # Backend FastAPI expects these exact keys: document_type, parties, terms, dates
        payload = {
            "document_type": doc_type,
            "parties": parties,
            "terms": key_terms,
            "dates": effective_date
        }
        
        with st.spinner("Generating legal document with AI..."):
            try:
                # Backend FastAPI Server Call (Port 8000)
                response = requests.post("http://127.0.0.1:8000/generate", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Document Generated Successfully!")
                    
                    document_text = result.get("generated_document", "") or result.get("document", "")
                    clean_text = sanitize_text(document_text)
                    
                    # Live Preview
                    st.markdown("### Document Preview")
                    html_preview = format_html_preview(clean_text)
                    st.markdown(html_preview, unsafe_allow_html=True)
                    
                    # Download Options
                    st.markdown("---")
                    st.markdown("### Download Options")
                    
                    col_d1, col_d2, col_d3 = st.columns(3)
                    
                    # DOCX Download
                    docx_file = format_docx(clean_text)
                    col_d1.download_button(
                        label="📄 Download DOCX",
                        data=docx_file,
                        file_name=f"{doc_type.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                    # PDF Download
                    pdf_file = format_pdf(clean_text)
                    col_d2.download_button(
                        label="📕 Download PDF",
                        data=bytes(pdf_file),
                        file_name=f"{doc_type.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                    
                    # TXT Download
                    col_d3.download_button(
                        label="📝 Download TXT",
                        data=clean_text,
                        file_name=f"{doc_type.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Could not connect to backend server. Error: {e}")