import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. INITIALISATION (CORRIGE L'ERREUR ATTRIBUTERROR) ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

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

# --- 5. DESIGN "GRANDE FÊTE" (BALLONS, ÉTOILES, CONFETTIS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* FOND ARC-EN-CIEL DOUX */
    .stApp { 
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); 
    }

    /* TITRE MAGIQUE GÉANT */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One', cursive !important;
        color: #9575CD !important; 
        font-size: 50px !important;
        text-shadow: 4px 4px 0px white;
        margin-top: -20px;
        margin-bottom: 20px;
    }

    /* BOUTONS GÉANTS POUR TÉLÉPHONE */
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

    .stButton > button:active {
        transform: translateY(8px);
        box-shadow: 0px 2px 0px #D1C4E9 !important;
    }

    /* --- DÉCORATIONS ANIMÉES --- */
    .ballon { position: fixed; font-size: 50px; z-index: 0; animation: monte 10s linear infinite; opacity: 0.7; }
    .etoile { position: fixed; font-size: 30px; z-index: 0; animation: brille 2s ease-in-out infinite; opacity: 0.8; }
    
    @keyframes monte {
        0% { transform: translateY(100vh) rotate(0deg); }
        100% { transform: translateY(-100vh) rotate(20deg); }
    }
    @keyframes brille {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.3); opacity: 1; }
    }

    /* CACHER LES TRUCS MOCHES */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 2rem !important; }
    </style>

    <div class="ballon" style="left:5%; animation-duration: 12s;">🎈</div>
    <div class="ballon" style="left:85%; animation-duration: 8s;">🎈</div>
    <div class="etoile" style="top:15%; left:10%;">⭐</div>
    <div class="etoile" style="top:40%; right:15%;">✨</div>
    <div class="etoile" style="bottom:20%; left:20%;">🌟</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 6. INTERFACE DE JEU ---

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# Menu du haut (Gros boutons 2x2)
m1, m2 = st.columns(2)
with m1:
    if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
    if st.button("📖 DICO"): st.session_state.mode = "dict"
with m2:
    if st.button("🧮 CALCUL"): st.session_state.mode = "calc"
    if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"

st.markdown("<br>", unsafe_allow_html=True)

# --- CONTENU DYNAMIQUE ---
if st.session_state.mode == "jeu":
    # 3 Univers principaux
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

    # Grille de contenu (2 colonnes pour téléphone)
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

elif st.session_state.mode == "calc":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Nombre :", 0, 10)
    if st.button("ÉCOUTER"): parler(n)

elif st.session_state.mode == "dict":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    m = st.text_input("Mot :")
    if st.button("🌟 EXPLIQUE"):
        if m: d = ia_magique(m, "dico"); st.info(d); parler(d)

elif st.session_state.mode == "ia":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    q = st.text_input("Question :")
    if st.button("DOUDOU ?"):
        if q: r = ia_magique(q, "doudou"); st.info(r); parler(r)
