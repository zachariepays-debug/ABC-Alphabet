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
    system_instruction = "Tu es un doudou gentil pour enfant de 3 ans. Phrases très courtes et joyeuses."
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

# --- 4. DESIGN ULTRA-BEAU POUR BÉBÉS (NOUVEAU FOND MAGIQUE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* LE FOND : Un paysage de dessin animé (Ciel, Nuages, Soleil) */
    .stApp { 
        background: 
            radial-gradient(circle at 10% 10%, #FFF9C4 0%, transparent 15%), /* Petit soleil doux */
            radial-gradient(circle at 90% 15%, #FFFFFF 0%, transparent 10%), /* Nuage 1 */
            radial-gradient(circle at 80% 10%, #FFFFFF 0%, transparent 12%), /* Nuage 1 bis */
            linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2); /* Ton arc-en-ciel animé */
        background-size: 100% 100%, 100% 100%, 100% 100%, 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    /* CONTENEUR PRINCIPAL : Style Nuage Blanc */
    .block-container {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50px;
        padding: 40px !important;
        margin-top: 30px;
        border: 8px solid rgba(255, 255, 255, 0.8);
    }

    /* TITRES ET TEXTES */
    .titre-enfant { 
        text-align: center; 
        font-size: 55px !important; 
        color: #FF69B4 !important; /* Rose Bonbon */
        font-family: 'Fredoka One', cursive !important;
        text-shadow: 4px 4px 0px white;
        margin-bottom: 30px;
    }
    
    label, p, .stMarkdown { 
        color: #4A4A4A !important; 
        font-family: 'Fredoka One', cursive !important;
        font-size: 20px !important;
    }

    /* BOUTONS STYLE "BONBON" ET "REBOND" */
    .stButton > button { 
        background: white !important; 
        border: 6px solid #FF69B4 !important; 
        border-radius: 35px !important; 
        color: #FF69B4 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 22px !important; 
        height: 85px !important; 
        width: 100% !important; 
        box-shadow: 0px 8px 0px #FF69B4 !important; 
        transition: all 0.2s ease;
    }
    
    /* Effet quand on passe la souris (Rebondit) */
    .stButton > button:hover {
        transform: scale(1.05);
        background: #FFF0F5 !important;
    }
    
    /* Effet quand on clique (S'enfonce) */
    .stButton > button:active {
        transform: translateY(6px);
        box-shadow: 0px 2px 0px #FF69B4 !important;
    }

    /* COULEURS SPÉCIFIQUES PAR BOUTON */
    div[data-testid="stColumn"]:nth-of-type(1) .stButton > button { border-color: #8A63FF !important; color: #8A63FF !important; box-shadow: 0px 8px 0px #8A63FF !important; } /* Ecole */
    div[data-testid="stColumn"]:nth-of-type(2) .stButton > button { border-color: #4CAF50 !important; color: #4CAF50 !important; box-shadow: 0px 8px 0px #4CAF50 !important; } /* Calculs */
    div[data-testid="stColumn"]:nth-of-type(3) .stButton > button { border-color: #FF9800 !important; color: #FF9800 !important; box-shadow: 0px 8px 0px #FF9800 !important; } /* Dict */

    .btn-dossier button { background: #FFF9C4 !important; border-color: #FBC02D !important; color: #F57F17 !important; }
    .btn-objet button { background: #E1F5FE !important; border-color: #03A9F4 !important; color: #01579B !important; }
    .btn-retour button { background: #FFEBEE !important; border-color: #F44336 !important; color: #B71C1C !important; }
    </style>
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

st.write("---")

# --- MODES ---
if st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>Ma Calculatrice 🧮</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER LE NOMBRE"): parler(n)

elif st.session_state.mode == "dict":
    st.markdown("<h1 class='titre-enfant'>Définition 📖</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    mot_saisi = st.text_input("Écris un mot :")
    if st.button("🌟 EXPLIQUE-MOI"):
        if mot_saisi:
            definition = ia_magique(mot_saisi, mode="dico")
            st.success(definition); parler(definition)

elif st.session_state.mode == "ia":
    st.markdown("<h1 class='titre-enfant'>Doudou IA 🤖</h1>", unsafe_allow_html=True)
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
        st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
        if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h1 class='titre-enfant'>{'✨ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'MONDE MAGIQUE'}</h1>", unsafe_allow_html=True)
    
    if isinstance(contenu, dict):
        for k, v in contenu.items():
            if isinstance(v, dict):
                st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
                if st.button(k): st.session_state.chemin.append(k); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
                if st.button(k): parler(v)
                st.markdown('</div>', unsafe_allow_html=True)
