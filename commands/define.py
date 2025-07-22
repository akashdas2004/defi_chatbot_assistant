from education.glossary import glossary

def handle_define(term: str) -> str:
    key = term.strip().lower()
    if key in glossary:
        return f"📚 *{key.capitalize()}*\n{glossary[key]}"
    else:
        return f"❓ No definition found for '{term}'. Try /explain {term} for an AI-powered answer." 