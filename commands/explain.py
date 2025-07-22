from education.glossary import glossary
from education.gemini_explainer import ask_gemini

def handle_explain(term: str):
    key = term.strip().lower()
    if key in glossary:
        return f"📚 {key.capitalize()}:\n{glossary[key]}"
    else:
        return ask_gemini(term) 