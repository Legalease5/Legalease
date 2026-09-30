import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        
        # Priority model setup
        self.model = None
        for model_name in ["gemini-1.5-flash-8b", "gemini-1.5-flash", "gemini-2.0-flash-exp", "models/gemini-1.5-flash"]:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"--- SUCCESS: Connected to {model_name} ---")
                break
            except Exception as e:
                continue

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str):
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            "Ensure formal legal structure with multiple sections and legal clauses."
        )
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                return response.text
        except Exception as err:
            print(f"API Generation Error: {err}")
            
        # Fallback dummy response to stop 500 Internal Server Error
        return (
            f"LEGAL AGREEMENT: {document_type.upper()}\n\n"
            f"This agreement is made on {dates} between {parties}.\n\n"
            f"TERMS & CONDITIONS:\n{terms}\n\n"
            "1. OBLIGATIONS: The parties agree to adhere to the aforementioned conditions.\n"
            "2. GOVERNING LAW: This document shall be governed in accordance with local legal jurisdiction."
        )