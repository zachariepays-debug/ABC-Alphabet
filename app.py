import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. INITIALISATION ---
if 'mode' not in st.session_state: st.session_state.mode = "accueil"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# --- 2. CONFIGURATION PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

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

# --- 4. LOGIQUE IA (VERSION DOUDOU ENFANT) ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY: return "Clé magique ?"
    
    # Nouvelles instructions pour que l'IA parle comme un enfant/doudou
    if mode == "doudou":
        system_instruction = (
            "Tu es Doudou, un petit ourson en peluche qui parle à un enfant de 3 ans. "
            "Parle de manière très mignonne et simple. Utilise des mots comme 'Coucou', "
            "'Copain', 'Câlin', 'Hihi'. Fais des phrases très courtes. "
            "Tu ne sais pas tout, tu es juste un petit doudou gentil."
        )
    else:
        system_instruction = "Tu es un dictionnaire pour enfants. Donne une définition très simple en une phrase."

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {
        "model": "mistral-tiny", 
        "messages": [
            {"role": "system", "content": system_instruction}, 
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Doudou fait dodo... zzz"

# --- 5. DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    .titre-enfant { text-align: center; font-family: 'Fredoka One', cursive !important; color: #9575CD !important; font-size: 50px !important; text-shadow: 4px 4px 0px white; }
    .phrase-bienvenue { text-align: center; font-family: 'Fredoka One', cursive !important; color: #5E35B1; font-size: 28px !important; line-height: 1.4; margin-bottom: 30px; }
    .stButton > button { background: white !important; border: 5px solid #9575CD !important; border-radius: 40px !important; color: #5E35B1 !important; font-family: 'Fredoka One', cursive !important; font-size: 22px !important; min-height: 90px !important; width: 100% !important; box-shadow: 0px 8px 0px #D1C4E9 !important; margin-bottom: 15px !important; }
    .ballon { position: fixed; font-size: 45px; z-index: 0; animation: monte 10s linear infinite; opacity: 0.6; }
    @keyframes monte { 0% { transform: translateY(110vh); } 100% { transform: translateY(-110vh); } }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    <div class="ballon" style="left:5%;">🎈</div>
    <div class="ballon" style="left:85%; animation-delay: 4s;">🎈</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 6. NAVIGATION ---

if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='phrase-bienvenue'>Bonjour !<br>Où veux-tu aller <b>pour</b> t'amuser aujourd'hui ?</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []; st.rerun()
        if st.button("🤖 DOUDOU IA"): st.session_state.mode = "ia"; st.rerun()
    with c2:
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()
        if st.button("📖 DICO"): st.session_state.mode = "dict"; st.rerun()

elif st.session_state.mode == "ia":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("### 🤖 Parle avec Doudou")
    q = st.text_input("Dis quelque chose à Doudou :")
    if st.button("RÉPONDRE"):
        if q:
            reponse = ia_magique(q, "doudou")
            st.info(reponse)
            parler(reponse) # Doudou parle toujours !

elif st.session_state.mode == "dict":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("### 📖 Le Dico (Muet)")
    m = st.text_input("Quel mot veux-tu comprendre ?")
    if st.button("VOIR"):
        if m:
            definition = ia_magique(m, "dico")
            st.success(definition) # Pas de fonction parler() ici

# Le reste du code (jeu, calc) ne change pas...
