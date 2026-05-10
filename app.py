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
    if not MISTRAL_API_KEY:
        return "Branche ma clé magique !"
    system_instruction = "Tu es un doudou gentil pour enfant. Phrases courtes et joyeuses."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Mode={mode}. Réponds à : {prompt}"}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Le doudou se repose..."

# --- 4. DESIGN "FÊTE MAGIQUE" (BALLONS & CONFETTIS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* LE FOND : Dégradé pastel doux */
    .stApp { 
        background: linear-gradient(135deg, #E0F7FA 0%, #F3E5F5 50%, #FFF9C4 100%);
        overflow: hidden;
    }

    /* CRÉATION DES BALLONS ET CONFETTIS EN ARRIÈRE-PLAN */
    .stApp::before {
        content: '🎈'; position: fixed; top: 10%; left: 5%; font-size: 50px; animation: float 6s ease-in-out infinite; z-index: 0;
    }
    .stApp::after {
        content: '🎈'; position: fixed; bottom: 15%; right: 5%; font-size: 60px; animation: float 8s ease-in-out infinite; z-index: 0;
    }
    
    /* Animation de flottement */
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }

    /* CONTENEUR PRINCIPAL : On le rend invisible pour voir le décor derrière */
    .block-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 20px !important;
    }

    /* TITRE "MONDE MAGIQUE" */
    .titre-enfant { 
        text-align: center; 
        font-size: 60px !important; 
        color: #9575CD !important; 
        font-family: 'Fredoka One', cursive !important;
        text-shadow: 3px 3px 0px white, -1px -1px 0px #7E57C2;
        margin-bottom: 20px;
    }

    /* BOUTONS STYLE "IMAGE" (Bords violets, fond blanc, écriture simple) */
    .stButton > button { 
        background: white !important; 
        border: 4px solid #9575CD !important; 
        border-radius: 40px !important; 
        color: #5E35B1 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 22px !important; 
        height: 75px !important; 
        width: 100% !important; 
        box-shadow: 0px 6px 0px #D1C4E9 !important; 
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 15px rgba(149, 117, 205, 0.3) !important;
    }

    /* DÉCORS SUPPLÉMENTAIRES (Etoiles et confettis) */
    .decor {
        position: fixed; font-size: 20px; pointer-events: none; opacity: 0.6;
    }

    /* CHAMPS DE TEXTE */
    input { 
        border-radius: 20px !important; 
        border: 3px solid #9575CD !important;
        font-family: 'Fredoka One', cursive !important;
    }
    </style>
    
    <div class="decor" style="top:20%; left:80%;">⭐</div>
    <div class="decor" style="top:50%; left:10%;">✨</div>
    <div class="decor" style="top:80%; left:40%;">❤️</div>
    <div class="decor" style="top:15%; left:30%;">🌟</div>
    <div class="decor" style="bottom:10%; left:70%;">🎉</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. NAVIGATION ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
with c2: 
    if st.button("🧮 CALCULS"): st.session_state.mode = "calc"
with c3: 
    if st.button("📖 DÉFINITION"): st.session_state.mode = "dict"
with c4: 
    if st.button("🤖 DOUDOU IA"): st.session_state.mode = "ia"

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# --- MODES ---
if st.session_state.mode == "calc":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER LE NOMBRE"): parler(n)

elif st.session_state.mode == "dict":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    mot_saisi = st.text_input("Écris un mot :")
    if st.button("🌟 EXPLIQUE-MOI"):
        if mot_saisi:
            definition = ia_magique(mot_saisi, mode="dico")
            st.success(definition); parler(definition)

elif st.session_state.mode == "ia":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    q = st.text_input("Pose une question :")
    if st.button("PARLER AU DOUDOU"):
        rep = ia_magique(q, mode="doudou")
        st.info(rep); parler(rep)

else:
    # Système de dossiers univers
    cols = st.columns(3)
    btns = ["🦁 NATURE", "🌍 MONDE", "🎁 JEUX"]
    for i, t in enumerate(btns):
        if cols[i].button(t): st.session_state.slide, st.session_state.chemin = i + 2, []

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})

    if st.session_state.chemin:
        if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    st.write(f"### ✨ {st.session_state.chemin[-1] if st.session_state.chemin else ''}")
    
    if isinstance(contenu, dict):
        # Affichage des boutons de dossiers ou d'objets
        for k, v in contenu.items():
            if isinstance(v, dict):
                if st.button(f"📁 {k}"): 
                    st.session_state.chemin.append(k)
                    st.rerun()
            else:
                if st.button(f"🔊 {k}"): parler(v)
