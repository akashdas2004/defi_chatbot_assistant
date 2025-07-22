import os
import google.generativeai as genai
from education.glossary import glossary

# You can move this to settings.yaml or .env if you prefer
GEMINI_API_KEY = "AIzaSyAs7zohF2ZSNLDZ_9MwdPkbHujl50VCnWE"
MODEL_NAME = "gemini-1.5-flash"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def ask_gemini(term: str) -> str:
    """
    Uses Gemini to explain a DeFi term in simple language.
    Falls back to glossary if available.
    """
    key = term.strip().lower()

    # 🔍 Check glossary first for fast static answer
    if key in glossary:
        return f"📚 *{key.capitalize()}*\n{glossary[key]}"

    # 🧠 Ask Gemini LLM
    try:
        prompt = f"Explain this DeFi concept in simple beginner-friendly language: {term}"
        response = model.generate_content(prompt)
        explanation = response.text.strip()

        if not explanation:
            return "🤖 Gemini didn't return a valid response."

        return f"📖 *{term.title()} (via Gemini)*\n{explanation}"

    except Exception as e:
        return f"⚠️ Gemini API Error: {e}" 