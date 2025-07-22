import json
import os

LANG_DATA = {}

def load_languages():
    for file in os.listdir("lang"):
        if file.endswith(".json"):
            lang_code = file.split(".")[0]
            with open(f"lang/{file}", "r", encoding="utf-8") as f:
                LANG_DATA[lang_code] = json.load(f)

def t(key, lang="en"):
    return LANG_DATA.get(lang, LANG_DATA["en"]).get(key, key) 