import streamlit as st
from gtts import gTTS
import base64
import io
import requests
import time
import random

# --- 1. INITIALISATION ---
if 'mode' not in st.session_state: st.session_state.mode = "accueil"
if 'chemin' not in st.session_state: st.session_state.chemin = []
if 'calc_val' not in st.session_state: st.session_state.calc_val = ""
if 'dino_score' not in st.session_state: st.session_state.dino_score = 0

# --- 2. CONFIGURATION PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

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

# --- 4. LOGIQUE IA & VOIX ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY: return "Clé magique ?"
    system = "Dictionnaire enfantin. Court." if mode == "dico" else "Doudou, ourson mimi."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Oups..."

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
    .titre-enfant { text-align: center; font-family: 'Fredoka One'; color: #5E35B1; font-size: 40px; text-shadow: 2px 2px white; margin-bottom: 20px;}
    .stButton > button { 
        background: white !important; border: 4px solid #5E35B1 !important; border-radius: 25px !important; 
        color: #5E35B1 !important; font-family: 'Fredoka One' !important; font-size: 20px !important; 
        min-height: 80px !important; margin-bottom: 10px !important; box-shadow: 0px 5px 0px #D1C4E9 !important;
    }
    .calc-screen { background: white; border: 4px solid #5E35B1; border-radius: 15px; padding: 15px; text-align: left; font-size: 40px; color: #5E35B1; min-height: 70px; }
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
        if st.button("🦖 JEU DINO"): st.session_state.mode = "dino"; st.rerun()

# --- MODE JEU DINO ---
elif st.session_state.mode == "dino":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("<h2 style='text-align:center;'>🦖 SAUT DU DINO</h2>", unsafe_allow_html=True)
    
    # Simulation simplifiée de jeu
    game_col1, game_col2, game_col3 = st.columns([1,2,1])
    with game_col2:
        st.write(f"### Score : {st.session_state.dino_score}")
        obstacle = random.choice(["🌵", "  ", "  "])
        st.markdown(f"<div style='font-size:100px; text-align:center; border-bottom: 5px solid brown;'>🦖 &nbsp;&nbsp;&nbsp; {obstacle}</div>", unsafe_allow_html=True)
        
        if st.button("🚀 SAUTER !", use_container_width=True):
            if obstacle == "🌵":
                st.balloons()
                st.session_state.dino_score += 1
                parler("Bravo !")
            else:
                st.session_state.dino_score += 1
            st.rerun()

# --- MODE MACHINE À PHRASES ---
elif st.session_state.mode == "parleur":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    phrase = st.text_area("Tape ta phrase :", height=150)
    if st.button("🔊 PARLER"): parler(phrase)

# --- MODE APPRENTISSAGE ---
elif st.session_state.mode == "jeu":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    if not st.session_state.chemin:
        u1, u2 = st.columns(2)
        with u1:
            if st.button("🏫 L'ÉCOLE"): st.session_state.chemin = ["ECOLE"]; st.rerun()
            if st.button("🦁 LA NATURE"): st.session_state.chemin = ["NATURE"]; st.rerun()
        with u2:
            if st.button("🌍 LE MONDE"): st.session_state.chemin = ["MONDE"]; st.rerun()
            if st.button("🎁 LES JEUX"): st.session_state.chemin = ["JEUX"]; st.rerun()

    MASTER_DATA = {"ECOLE": ECOLE_DATA, "NATURE": NATURE_DATA, "MONDE": MONDE_DATA, "JEUX": JEUX_DATA}
    contenu = MASTER_DATA
    for d in st.session_state.chemin:
        if isinstance(contenu, dict): contenu = contenu.get(d, {})

    if st.session_state.chemin and st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    if isinstance(contenu, dict) and st.session_state.chemin:
        items = list(contenu.items())
        for i in range(0, len(items), 2):
            ca, cb = st.columns(2)
            with ca:
                k, v = items[i]
                if st.button(f"{'📁' if isinstance(v, dict) else '🔊'} {k}"):
                    if isinstance(v, dict): st.session_state.chemin.append(k); st.rerun()
                    else: parler(v)
            if i + 1 < len(items):
                with cb:
                    k, v = items[i+1]
                    if st.button(f"{'📁' if isinstance(v, dict) else '🔊'} {k}"):
                        if isinstance(v, dict): st.session_state.chemin.append(k); st.rerun()
                        else: parler(v)

# --- MODE CALCULS ---
elif st.session_state.mode == "calc":
    if st.button("🏠 QUITTER"): st.session_state.mode = "accueil"; st.session_state.calc_val = ""; st.rerun()
    st.markdown(f"<div class='calc-screen'>{st.session_state.calc_val if st.session_state.calc_val else '0'}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    btns = [("1","2","3"), ("4","5","6"), ("7","8","9"), ("+","0","-")]
    for row in btns:
        with c1: 
            if st.button(row[0]): st.session_state.calc_val += row[0]; st.rerun()
        with c2: 
            if st.button(row[1]): st.session_state.calc_val += row[1]; st.rerun()
        with c3: 
            if st.button(row[2]): st.session_state.calc_val += row[2]; st.rerun()
    if st.button("⭐ ÉGAL"):
        try:
            res = eval(st.session_state.calc_val)
            st.session_state.calc_val = str(res); parler(f"Ça fait {res}")
        except: st.session_state.calc_val = ""; st.rerun()

# --- MODE DICO ---
elif st.session_state.mode == "dict":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    m = st.text_input("Mot :")
    if st.button("🌟 VOIR"):
        if m: res = ia_magique(m, "dico"); st.write(f"### {res}"); parler(res)

# --- MODE DOUDOU ---
elif st.session_state.mode == "ia":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    q = st.text_input("Dis à Doudou :")
    if st.button("RÉPONDRE"):
        if q: res = ia_magique(q, "doudou"); st.info(res); parler(res)
