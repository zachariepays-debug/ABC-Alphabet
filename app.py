import streamlit as st
from gtts import gTTS
import base64
import io
import requests
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈✨", layout="wide", initial_sidebar_state="collapsed")

try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 2. ÉCRAN DE CHARGEMENT ARC-EN-CIEL DÉCORÉ ---
if 'chargement_fini' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
            
            .loading-screen {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
                background-size: 400% 400%; animation: grad 15s ease infinite;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                z-index: 9999; font-family: 'Fredoka One', cursive;
            }
            @keyframes grad { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
            
            .ballon-load { font-size: 120px; animation: bounce 1s infinite alternate; }
            @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-40px); } }
            
            .txt-load { color: #2C3E50; font-size: 35px; margin-top: 30px; text-shadow: 2px 2px 0px white; }
            
            .rainbow-bar { width: 300px; height: 20px; background: white; border-radius: 10px; margin-top: 20px; overflow: hidden; border: 3px solid #FFF; }
            .rainbow-progress { width: 100%; height: 100%; background: linear-gradient(to right, #FF1493, #00BFFF, #00FF7F, #FFD700); animation: slide 2s linear infinite; }
            @keyframes slide { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
            </style>
            
            <div class="loading-screen">
                <div style="position:absolute; top:10%; left:10%; font-size:40px;">✨</div>
                <div style="position:absolute; top:20%; right:15%; font-size:40px;">🎈</div>
                <div style="position:absolute; bottom:20%; left:20%; font-size:40px;">⭐</div>
                <div class="ballon-load">🎈</div>
                <div class="txt-load">La magie arrive...</div>
                <div class="rainbow-bar"><div class="rainbow-progress"></div></div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(5)
    st.session_state.chargement_fini = True
    placeholder.empty()

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
    if not MISTRAL_API_KEY: return "Besoin de la clé magique !"
    sys = "Tu es un doudou gentil. Mode dico=def courte. Mode doudou=joyeux."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": sys}, {"role": "user", "content": f"Mode={mode}. {prompt}"}]}
    try:
        r = requests.post(url, json=data, headers=headers)
        return r.json()['choices'][0]['message']['content']
    except: return "Le doudou se repose..."

# --- 5. STYLE GLOBAL (CORRIGÉ POUR ÉVITER LE BUG) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp {{
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: grad_main 15s ease infinite;
    }}

    @keyframes grad_main {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Déco flottante en arrière-plan */
    .stApp::before {{
        content: '✨ 🎈 ⭐ ✨ 🎈 ⭐';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        font-size: 40px; line-height: 150px; word-spacing: 200px;
        color: rgba(255,255,255,0.3);
        pointer-events: none; z-index: -1;
    }}

    .titre-enfant {{ text-align: center; font-size: 42px !important; color: #8A63FF !important; font-family: 'Fredoka One', cursive !important; text-shadow: 2px 2px 0px white; }}
    .stButton > button {{ background: #FFF !important; border: 4px solid #8A63FF !important; border-radius: 20px !important; color: #8A63FF !important; font-family: 'Fredoka One', cursive !important; font-size: 20px !important; height: 70px !important; box-shadow: 0px 4px 0px #8A63FF !important; }}
    input {{ color: #000 !important; background: #FFF !important; border: 4px solid; border-image: linear-gradient(to right, #FF1493, #00BFFF, #00FF7F, #FFD700) 1; border-radius: 15px; font-size: 22px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

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

# Affichage des contenus (Calc, Dict, IA ou Dossiers)
if st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>Ma Calculatrice 🧮</h1>", unsafe_allow_html=True)
    n = st.number_input("Nombre :", 0, 10)
    if st.button("ÉCOUTER"): parler(n)
elif st.session_state.mode == "dict":
    st.markdown("<h1 class='titre-enfant'>Définition 📖</h1>", unsafe_allow_html=True)
    mot = st.text_input("Écris un mot :")
    if st.button("EXPLIQUE-MOI"):
        if mot: res = ia_magique(mot, "dico"); st.success(res); parler(res)
elif st.session_state.mode == "ia":
    st.markdown("<h1 class='titre-enfant'>Doudou IA 🤖</h1>", unsafe_allow_html=True)
    q = st.text_input("Pose une question gentille :")
    if st.button("PARLER"):
        if q: res = ia_magique(q, "doudou"); st.info(res); parler(res)
else:
    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})
    
    st.markdown(f"<h1 class='titre-enfant'>{'✨ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'MONDE MAGIQUE'}</h1>", unsafe_allow_html=True)
    
    if isinstance(contenu, dict):
        cols = st.columns(2)
        for idx, (k, v) in enumerate(contenu.items()):
            with cols[idx % 2]:
                if isinstance(v, dict):
                    if st.button(f"📁 {k}", key=k): st.session_state.chemin.append(k); st.rerun()
                else:
                    if st.button(f"🔊 {k}", key=k): parler(v)
