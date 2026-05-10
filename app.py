import streamlit as st
from gtts import gTTS
import base64
import io
import requests
import random

# --- 1. INITIALISATION ---
if 'mode' not in st.session_state: st.session_state.mode = "accueil"
if 'chemin' not in st.session_state: st.session_state.chemin = []
if 'calc_val' not in st.session_state: st.session_state.calc_val = ""
if 'dino_score' not in st.session_state: st.session_state.dino_score = 0
if 'ballon_h' not in st.session_state: st.session_state.ballon_h = 50
if 'secret_num' not in st.session_state: st.session_state.secret_num = random.randint(1, 10)

# --- 2. CONFIGURATION PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide")

try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 3. IMPORT DES DONNÉES ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 4. OUTILS (VOIX) ---
def parler(txt):
    if txt:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    .titre-enfant { text-align: center; font-family: 'Fredoka One'; color: #5E35B1; font-size: 40px; text-shadow: 2px 2px white; }
    .stButton > button { 
        background: white !important; border: 4px solid #5E35B1 !important; border-radius: 25px !important; 
        color: #5E35B1 !important; font-family: 'Fredoka One' !important; font-size: 20px !important; 
        min-height: 80px !important; margin-bottom: 10px !important; box-shadow: 0px 5px 0px #D1C4E9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---

if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎓 APPRENTISSAGE"): st.session_state.mode, st.session_state.chemin = "jeu", []; st.rerun()
        if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"; st.rerun()
        if st.button("🗣️ MACHINE À PHRASES"): st.session_state.mode = "parleur"; st.rerun()
    with c2:
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()
        if st.button("📖 DICO"): st.session_state.mode = "dict"; st.rerun()
        if st.button("🎮 JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()

# --- NOUVEAU DOSSIER JEUX ---
elif st.session_state.mode == "menu_jeux":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("<h2 style='text-align:center;'>🎮 CHOISIS TON JEU</h2>", unsafe_allow_html=True)
    cj1, cj2 = st.columns(2)
    if cj1.button("🦖 DINO SAUTEUR"): st.session_state.mode = "dino"; st.rerun()
    if cj1.button("🎈 MONTGOLFIÈRE"): st.session_state.mode = "balon"; st.rerun()
    if cj2.button("🔢 CHIFFRE CACHÉ"): st.session_state.mode = "cache"; st.rerun()

# --- JEU 1 : DINO ---
elif st.session_state.mode == "dino":
    if st.button("🔙 MENU JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()
    obs = random.choice(["🌵", "  ", "  "])
    st.markdown(f"<div style='font-size:80px; text-align:center;'>Score: {st.session_state.dino_score}<br>🦖 &nbsp;&nbsp;&nbsp; {obs}</div>", unsafe_allow_html=True)
    if st.button("🚀 SAUTER !"):
        if obs == "🌵": st.session_state.dino_score += 1; st.balloons(); parler("Super !")
        else: st.session_state.dino_score += 1
        st.rerun()

# --- JEU 2 : MONTGOLFIÈRE ---
elif st.session_state.mode == "balon":
    if st.button("🔙 MENU JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()
    st.markdown(f"<div style='height:300px; position:relative; background:skyblue; border-radius:20px;'> <div style='position:absolute; bottom:{st.session_state.ballon_h}px; left:45%; font-size:50px;'>🎈</div> </div>", unsafe_allow_html=True)
    if st.button("⬆️ VOLER !"):
        st.session_state.ballon_h = min(250, st.session_state.ballon_h + 40)
        if st.session_state.ballon_h >= 240: st.snow(); parler("Tu touches les nuages !")
        st.rerun()
    else:
        st.session_state.ballon_h = max(10, st.session_state.ballon_h - 10)

# --- JEU 3 : CHIFFRE CACHÉ ---
elif st.session_state.mode == "cache":
    if st.button("🔙 MENU JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()
    st.write("### Devine le chiffre entre 1 et 10 !")
    choix = st.number_input("Ton chiffre :", min_value=1, max_value=10)
    if st.button("VÉRIFIER"):
        if choix == st.session_state.secret_num:
            st.success("BRAVO ! C'était bien ça ! 🎉")
            parler(f"Bravo ! C'était le {choix}")
            st.session_state.secret_num = random.randint(1, 10)
        elif choix < st.session_state.secret_num: st.write("C'est plus grand ! ⬆️")
        else: st.write("C'est plus petit ! ⬇️")

# (Les autres modes APPRENTISSAGE, CALC, DICO, PARLEUR restent identiques au code précédent)
