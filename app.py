import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. CONFIGURATION & RÉCUPÉRATION DU SECRET ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# On récupère la clé depuis les secrets de Streamlit
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    st.error("La clé secrète MISTRAL_API_KEY est introuvable dans les paramètres !")
    MISTRAL_API_KEY = None

# --- 2. LOGIQUE IA (MISTRAL) ---
def demander_au_doudou(question):
    if not MISTRAL_API_KEY:
        return "Oh non ! Mon cerveau magique n'est pas branché."
        
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": "Tu es un doudou magique et gentil pour un bébé de 3 ans. Tu parles de manière très simple, douce et joyeuse. Tu fais des réponses très courtes."},
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Je fais un petit dodo, reviens me voir plus tard !"

# ... (Le reste du code pour le design et les boutons reste identique)
