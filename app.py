import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="L'Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- DESIGN "VIVANT & ANIMÉ" ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000000; } 
    
    /* Animation de pulsation pour les boutons */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .stButton > button {
        width: 100%; height: 115px !important;
        font-size: 24px !important; font-weight: 900 !important;
        border-radius: 30px !important;
        border: 4px solid #ffffff !important;
        text-transform: uppercase;
        animation: pulse 3s infinite ease-in-out;
        transition: 0.3s !important;
    }
    
    /* Couleurs Néons */
    div[data-testid="stVerticalBlock"] > div:nth-child(odd) button { background: linear-gradient(45deg, #00F2FE, #4FACFE) !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(even) button { background: linear-gradient(45deg, #F093FB, #F5576C) !important; color: white !important; }
    
    /* Barre de navigation (Dots) comme sur ta photo */
    .nav-dots {
        display: flex; justify-content: center; margin-bottom: 20px;
    }
    .dot {
        height: 15px; width: 15px; background-color: #555; border-radius: 50%; display: inline-block; margin: 0 10px;
    }
    .active-dot { background-color: #FF0055; box-shadow: 0 0 10px #FF0055; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES MASSIVE ---
DATABASE = {
    "🦁 Le Zoo": {
        "Savane": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre"},
        "Forêt": {"🦊":"Renard","🦌":"Cerf","🐺":"Loup","🐻":"Ours"},
        "Banquise": {"🐧":"Manchot","🐻‍❄️":"Ours Polaire","🦭":"Phoque"}
    },
    "⚽ Sports & Fun": {
        "Jeux": {"⚽":"Foot","🏀":"Basket","🎾":"Tennis","🥊":"Boxe","🚲":"Vélo"},
        "Musique": {"🎹":"Piano","🎸":"Guitare","🥁":"Batterie","🎺":"Trompette","🎻":"Violon"}
    },
    "🪐 Nature & Espace": {
        "Météo": {"☀️":"Soleil","🌧️":"Pluie","⚡":"Orage","❄️":"Neige","🌈":"Arc-en-ciel"},
        "Espace": {"🌍":"Terre","🚀":"Fusée","🌙":"Lune","🪐":"Saturne","👽":"Alien"}
    }
}

# --- LOGIQUE ---
if 'page' not in st.session_state: st.session_state.page = "menu"
if 'sub' not in st.session_state: st.session_state.sub = ""

def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.encodebytes(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def nav(p, s=""):
    st.session_state.page = p
    st.session_state.sub = s
    st.rerun()

# --- INTERFACE ---

# Affichage des "Dots" de navigation
active = "active-dot" if st.session_state.page == "menu" else ""
st.markdown(f"""
    <div class="nav-dots">
        <span class="dot {active}"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "menu":
    st.markdown("<h1 style='text-align:center; color:#00F2FE;'>👑 EMPIRE ANIMÉ</h1>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    categories = list(DATABASE.keys()) + ["🔤 Alphabet", "🔢 Chiffres", "🌍 Drapeaux"]
    
    for i, cat in enumerate(categories):
        with cols[i % 2]:
            if st.button(cat):
                if cat in DATABASE: nav(cat)
                else: nav(cat.lower())

elif st.session_state.page in DATABASE:
    if st.button("⬅️ MENU"): nav("menu")
    data_cat = DATABASE[st.session_state.page]
    
    if st.session_state.sub == "":
        cols = st.columns(2)
        for i, sub in enumerate(data_cat.keys()):
            with cols[i % 2]:
                if st.button(sub): nav(st.session_state.page, sub)
    else:
        if st.button("⬅️ RETOUR"): nav(st.session_state.page, "")
        items = data_cat[st.session_state.sub]
        cols = st.columns(2)
        for i, (e, n) in enumerate(items.items()):
            with cols[i % 2]:
                if st.button(f"{e}\n{n}"): parler(n)

# Sections Alphabet / Chiffres / Drapeaux (Simplifié pour l'exemple)
elif st.session_state.page == "alphabet":
    if st.button("⬅️ MENU"): nav("menu")
    cols = st.columns(4)
    for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        with cols[random.randint(0,3)]:
            if st.button(l): parler(l)
