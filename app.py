import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. INITIALISATION (Obligatoire pour éviter les erreurs) ---
if 'mode' not in st.session_state: 
    st.session_state.mode = "accueil"  # On commence maintenant par l'accueil
if 'slide' not in st.session_state: 
    st.session_state.slide = 1
if 'chemin' not in st.session_state: 
    st.session_state.chemin = []

# --- 2. CONFIGURATION PAGE ---
st.set_page_config(page_title="FÊTE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# Récupération de la clé Mistral
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 3. IMPORT DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 4. LOGIQUE IA ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY: return "Clé magique ?"
    system_instruction = "Tu es un doudou gentil. Phrases très courtes."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": f"Mode={mode}. {prompt}"}]}
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Le doudou dort..."

# --- 5. DESIGN "GRANDE FÊTE" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }

    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One', cursive !important;
        color: #9575CD !important; 
        font-size: 55px !important;
        text-shadow: 4px 4px 0px white;
        margin-top: 20px;
    }

    .phrase-bienvenue {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        color: #5E35B1;
        font-size: 30px !important;
        margin-bottom: 40px;
    }

    .stButton > button { 
        background: white !important; 
        border: 5px solid #9575CD !important; 
        border-radius: 40px !important; 
        color: #5E35B1 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 24px !important; 
        min-height: 100px !important; 
        width: 100% !important; 
        box-shadow: 0px 10px 0px #D1C4E9 !important; 
        white-space: normal !important;
        margin-bottom: 20px !important;
    }

    .stButton > button:active { transform: translateY(8px); box-shadow: 0px 2px 0px #D1C4E9 !important; }

    /* DÉCORATIONS */
    .ballon { position: fixed; font-size: 50px; z-index: 0; animation: monte 12s linear infinite; opacity: 0.7; }
    .etoile { position: fixed; font-size: 30px; z-index: 0; animation: brille 2s ease-in-out infinite; }
    
    @keyframes monte {
        0% { transform: translateY(110vh) rotate(0deg); }
        100% { transform: translateY(-110vh) rotate(30deg); }
    }
    @keyframes brille { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }

    #MainMenu, footer, header {visibility: hidden;}
    </style>

    <div class="ballon" style="left:10%; animation-delay: 0s;">🎈</div>
    <div class="ballon" style="left:80%; animation-delay: 3s;">🎈</div>
    <div class="etoile" style="top:20%; left:5%;">⭐</div>
    <div class="etoile" style="top:50%; right:5%;">✨</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 6. LOGIQUE DES PAGES ---

# --- PAGE D'ACCUEIL ---
if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='phrase-bienvenue'>Bonjour ! <br> Où veux-tu aller t'amuser aujourd'hui ?</p>", unsafe_allow_html=True)
    
    # Gros boutons de choix
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 L'ÉCOLE"):
            st.session_state.mode = "jeu"
            st.session_state.slide = 1
            st.rerun()
        if st.button("🤖 DOUDOU IA"):
            st.session_state.mode = "ia"
            st.rerun()
    with col2:
        if st.button("🧮 LES CALCULS"):
            st.session_state.mode = "calc"
            st.rerun()
        if st.button("📖 LE DICO"):
            st.session_state.mode = "dict"
            st.rerun()

# --- MODE JEU (UNIVERS) ---
elif st.session_state.mode == "jeu":
    if st.button("🏠 RETOUR À L'ACCUEIL"):
        st.session_state.mode = "accueil"
        st.rerun()

    # Les 3 Univers principaux
    u1, u2, u3 = st.columns(3)
    if u1.button("🦁 NATURE"): st.session_state.slide, st.session_state.chemin = 2, []
    if u2.button("🌍 MONDE"): st.session_state.slide, st.session_state.chemin = 3, []
    if u3.button("🎁 JEUX"): st.session_state.slide, st.session_state.chemin = 4, []

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})

    if st.session_state.chemin:
        if st.button("⬅️ RETOUR"): 
            st.session_state.chemin.pop()
            st.rerun()

    # Grille de contenu
    if isinstance(contenu, dict):
        items = list(contenu.items())
        for i in range(0, len(items), 2):
            col_a, col_b = st.columns(2)
            with col_a:
                k, v = items[i]
                if isinstance(v, dict):
                    if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                else:
                    if st.button(f"🔊 {k}"): parler(v)
            if i + 1 < len(items):
                with col_b:
                    k, v = items[i+1]
                    if isinstance(v, dict):
                        if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                    else:
                        if st.button(f"🔊 {k}"): parler(v)

# --- MODE CALCUL ---
elif st.session_state.mode == "calc":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER"): parler(n)

# --- MODE DICO ---
elif st.session_state.mode == "dict":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    m = st.text_input("Quel mot ?")
    if st.button("🌟 EXPLIQUE"):
        if m: d = ia_magique(m, "dico"); st.success(d); parler(d)

# --- MODE IA ---
elif st.session_state.mode == "ia":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    q = st.text_input("Parle au doudou :")
    if st.button("RÉPONDRE"):
        if q: r = ia_magique(q, "doudou"); st.info(r); parler(r)
