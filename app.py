import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# Récupération de la clé Mistral
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 2. IMPORT DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 3. LOGIQUE IA ---
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

# --- 4. DESIGN SPECIAL BÉBÉ & MOBILE (RÉPARE LES BOGUES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* FOND DÉGRADÉ MAGIQUE */
    .stApp { 
        background: linear-gradient(180deg, #E0F7FA 0%, #FFF9C4 100%); 
    }

    /* NETTOYAGE DES MARGES POUR TÉLÉPHONE */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* TITRE GÉANT */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One', cursive !important;
        color: #9575CD !important; 
        font-size: 45px !important;
        text-shadow: 3px 3px 0px white;
        margin-bottom: 20px;
    }

    /* RÉPARATION DES BOUTONS (FORCE LE TEXTE À RESTER DEDANS) */
    .stButton > button { 
        background: white !important; 
        border: 5px solid #9575CD !important; 
        border-radius: 30px !important; 
        color: #5E35B1 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 20px !important; 
        padding: 15px 10px !important;
        min-height: 90px !important; /* Bouton bien haut pour les doigts */
        width: 100% !important; 
        box-shadow: 0px 8px 0px #D1C4E9 !important; 
        white-space: normal !important; /* Empêche le texte de dépasser sur le côté */
        line-height: 1.2 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
    }

    .stButton > button:active {
        transform: translateY(6px);
        box-shadow: 0px 2px 0px #D1C4E9 !important;
    }

    /* DÉCO : BALLONS ANIMÉS */
    .ballon-deco {
        position: fixed; font-size: 40px; z-index: -1; animation: float 5s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    /* CACHER LE MENU STREAMLIT */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    
    <div class="ballon-deco" style="top:10%; right:10%;">🎈</div>
    <div class="ballon-deco" style="bottom:10%; left:5%; animation-delay: 2s;">🌟</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. INTERFACE ---

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# Navigation principale en gros boutons (2 par ligne)
c1, c2 = st.columns(2)
with c1:
    if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
    if st.button("📖 DICO"): st.session_state.mode = "dict"
with c2:
    if st.button("🧮 CALCUL"): st.session_state.mode = "calc"
    if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"

st.markdown("---")

# --- CONTENU DES UNIVERS ---
if st.session_state.mode == "jeu":
    # Les 3 Univers principaux
    u1, u2, u3 = st.columns(3)
    if u1.button("🦁 NATURE"): st.session_state.slide, st.session_state.chemin = 2, []
    if u2.button("🌍 MONDE"): st.session_state.slide, st.session_state.chemin = 3, []
    if u3.button("🎁 JEUX"): st.session_state.slide, st.session_state.chemin = 4, []

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})

    if st.session_state.chemin:
        if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    st.write(f"### ✨ {st.session_state.chemin[-1] if st.session_state.chemin else ''}")

    # Affichage des dossiers et objets en 2 colonnes pour téléphone
    if isinstance(contenu, dict):
        items = list(contenu.items())
        for i in range(0, len(items), 2):
            col_a, col_b = st.columns(2)
            # Premier item de la ligne
            with col_a:
                k, v = items[i]
                if isinstance(v, dict):
                    if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                else:
                    if st.button(f"🔊 {k}"): parler(v)
            # Deuxième item de la ligne (s'il existe)
            if i + 1 < len(items):
                with col_b:
                    k, v = items[i+1]
                    if isinstance(v, dict):
                        if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                    else:
                        if st.button(f"🔊 {k}"): parler(v)

# --- AUTRES MODES ---
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
