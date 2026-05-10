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

# --- 4. DESIGN OPTIMISÉ TÉLÉPHONE (FÊTE & BALLONS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* LE FOND */
    .stApp { 
        background: linear-gradient(135deg, #E0F7FA 0%, #F3E5F5 50%, #FFF9C4 100%);
    }

    /* BALLONS ADAPTATIFS */
    .stApp::before {
        content: '🎈'; position: fixed; top: 5%; left: 2%; font-size: 40px; animation: float 6s ease-in-out infinite; z-index: 0;
    }
    .stApp::after {
        content: '🎈'; position: fixed; bottom: 5%; right: 2%; font-size: 45px; animation: float 8s ease-in-out infinite; z-index: 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
    }

    /* CONTENEUR PRINCIPAL RESPONSIVE */
    .block-container {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 15px !important;
        margin-top: 10px;
    }

    /* TITRE ADAPTÉ AUX PETITS ÉCRANS */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One', cursive !important;
        color: #9575CD !important; 
        text-shadow: 2px 2px 0px white;
        line-height: 1.1;
    }

    /* TAILLES DE TEXTE SELON L'ÉCRAN */
    @media (max-width: 600px) {
        .titre-enfant { font-size: 35px !important; }
        .stButton > button { height: 60px !important; font-size: 16px !important; margin-bottom: 10px !important; }
        .decor { display: none; } /* On enlève les petits décors sur mobile pour ne pas gêner */
    }
    @media (min-width: 601px) {
        .titre-enfant { font-size: 60px !important; }
        .stButton > button { height: 80px !important; font-size: 22px !important; }
    }

    /* BOUTONS STYLE "IMAGE" */
    .stButton > button { 
        background: white !important; 
        border: 4px solid #9575CD !important; 
        border-radius: 25px !important; 
        color: #5E35B1 !important; 
        font-family: 'Fredoka One', cursive !important; 
        width: 100% !important; 
        box-shadow: 0px 5px 0px #D1C4E9 !important; 
        transition: 0.2s;
    }
    
    .stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0px 1px 0px #D1C4E9 !important;
    }

    /* CHAMPS DE TEXTE */
    input { 
        border-radius: 15px !important; 
        font-family: 'Fredoka One', cursive !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. NAVIGATION ---
# Utilisation de colonnes qui s'adaptent mieux
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📚 ECOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
with c2: 
    if st.button("🧮 CALC"): st.session_state.mode = "calc"
with c3: 
    if st.button("📖 DICO"): st.session_state.mode = "dict"
with c4: 
    if st.button("🤖 IA"): st.session_state.mode = "ia"

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# --- MODES ---
if st.session_state.mode == "calc":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Nombre :", 0, 10)
    if st.button("ÉCOUTER"): parler(n)

elif st.session_state.mode == "dict":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    mot_saisi = st.text_input("Un mot :")
    if st.button("🌟 EXPLIQUE"):
        if mot_saisi:
            definition = ia_magique(mot_saisi, mode="dico")
            st.success(definition); parler(definition)

elif st.session_state.mode == "ia":
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    q = st.text_input("Ta question :")
    if st.button("PARLER AU DOUDOU"):
        rep = ia_magique(q, mode="doudou")
        st.info(rep); parler(rep)

else:
    # Navigation dans les dossiers
    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    
    # Boutons des univers principaux
    col_u1, col_u2, col_u3 = st.columns(3)
    if col_u1.button("🦁 NATURE"): st.session_state.slide, st.session_state.chemin = 2, []
    if col_u2.button("🌍 MONDE"): st.session_state.slide, st.session_state.chemin = 3, []
    if col_u3.button("🎁 JEUX"): st.session_state.slide, st.session_state.chemin = 4, []

    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})

    if st.session_state.chemin:
        if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    st.write(f"### ✨ {st.session_state.chemin[-1] if st.session_state.chemin else ''}")
    
    if isinstance(contenu, dict):
        # On affiche les boutons un par un pour qu'ils soient bien gros sur mobile
        for k, v in contenu.items():
            if isinstance(v, dict):
                if st.button(f"📁 {k}"): 
                    st.session_state.chemin.append(k)
                    st.rerun()
            else:
                if st.button(f"🔊 {k}"): parler(v)
