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

# --- 3. LOGIQUE IA (DOUDOU & DICO) ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY:
        return "Branche ma clé magique !"
    
    # Consigne spéciale pour le dictionnaire
    system_instruction = """Tu es un doudou gentil. 
    Si mode=dico: Donne UNIQUEMENT la définition du mot de façon très simple pour un enfant de 3 ans. Pas de bonjour, juste la définition en une phrase courte.
    Si mode=doudou: Sois poli, joyeux et protecteur. Phrases très courtes."""
    
    instruction = f"Mode={mode}. Réponds à : {prompt}"
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": instruction}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Le doudou fait dodo..."

# --- 4. DESIGN ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .stApp {{ background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2); background-size: 400% 400%; animation: gradient 15s ease infinite; }}
    @keyframes gradient {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    
    .titre-enfant, label, p, .stMarkdown {{ color: #2C3E50 !important; font-family: 'Fredoka One', cursive !important; font-weight: bold !important; }}
    .titre-enfant {{ text-align: center; font-size: 42px !important; color: #8A63FF !important; text-shadow: 2px 2px 0px #FFFFFF; }}

    input {{ border: 4px solid !important; border-image: linear-gradient(to right, #FF1493, #00BFFF, #00FF7F, #FFD700) 1 !important; border-radius: 15px !important; background-color: white !important; font-size: 22px !important; }}
    
    .stButton > button {{ background: #FFFFFF !important; border: 4px solid #8A63FF !important; border-radius: 20px !important; color: #8A63FF !important; font-family: 'Fredoka One', cursive !important; font-size: 20px !important; height: 65px !important; width: 100% !important; box-shadow: 0px 4px 0px #8A63FF !important; }}
    .btn-dossier button {{ background: #FFF2B2 !important; border: 5px solid #FFCC00 !important; height: 100px !important; color: #D35400 !important; font-size: 24px !important; box-shadow: 0px 6px 0px #FFB300 !important; }}
    .btn-objet button {{ background: white !important; height: 80px !important; color: #2C3E50 !important; font-size: 22px !important; border: 3px solid #EEE !important; box-shadow: 0px 4px 0px #CCC !important; }}
    .btn-retour button {{ background: #FF1493 !important; color: white !important; border: 4px solid white !important; }}
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. LOGIQUE NAVIGATION ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
with c2: 
    if st.button("🧮 CALCULS"): st.session_state.mode = "calc"
with c3: 
    if st.button("📖 MOTS"): st.session_state.mode = "dict"
with c4: 
    if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"

st.write("---")

# --- AFFICHAGE DES MODES ---
if st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>Ma Calculatrice 🧮</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER"): parler(n)

elif st.session_state.mode == "dict":
    st.markdown("<h1 class='titre-enfant'>Mes Jolis Mots 📖</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    mot_saisi = st.text_input("Écris un mot :", key="input_dict")
    
    # Bouton spécial pour mobile
    if st.button("🌟 VOIR LA DÉFINITION"):
        if mot_saisi:
            definition = ia_magique(mot_saisi, mode="dico")
            st.success(definition)
            parler(definition)

elif st.session_state.mode == "ia":
    st.markdown("<h1 class='titre-enfant'>Doudou IA 🤖</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    q = st.text_input("Pose une question :")
    if st.button("PARLER AU DOUDOU"):
        rep = ia_magique(q, mode="doudou")
        st.info(rep)
        parler(rep)

else:
    # Système de jeu classique
    cols = st.columns(3)
    btns = ["🦁 NATURE", "🌍 MONDE", "🎁 JEUX"]
    for i, t in enumerate(btns):
        if cols[i].button(t): st.session_state.slide, st.session_state.chemin = i + 2, []

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping[st.session_state.slide]
    for d in st.session_state.chemin: contenu = contenu[d]

    if st.session_state.chemin:
        st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
        if st.button("⬅️ ON REVIENT !"): st.session_state.chemin.pop(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h1 class='titre-enfant'>{'✨ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'MONDE MAGIQUE'}</h1>", unsafe_allow_html=True)
    
    if isinstance(contenu, dict):
        for k, v in contenu.items():
            if isinstance(v, dict):
                st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
                if st.button(k): st.session_state.chemin.append(k); st.rerun()
            else:
                st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
                if st.button(k): parler(v)
