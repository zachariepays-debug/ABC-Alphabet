import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. INITIALISATION DES VARIABLES ---
if 'mode' not in st.session_state: st.session_state.mode = "accueil"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []
if 'calc_val' not in st.session_state: st.session_state.calc_val = ""

# --- 2. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# Clé API Mistral
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 3. IMPORT DES DONNÉES UNIVER ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 4. LOGIQUE IA (DOUDOU & DICO) ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY: return "Clé magique ?"
    
    if mode == "doudou":
        system = "Tu es Doudou, un petit ourson mimi. Parle comme un enfant de 3 ans. Phrases très courtes, mots gentils (Coucou, Câlin, Copain, Hihi)."
    else:
        system = "Tu es un dictionnaire simple. Donne UNIQUEMENT la définition, sans introduction ni bonjour. Une seule phrase courte."

    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Doudou dort..."

# --- 5. DESIGN & STYLE (MOBILE FIRST) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    .titre-enfant { text-align: center; font-family: 'Fredoka One', cursive; color: #9575CD; font-size: 42px; text-shadow: 3px 3px 0px white; margin-bottom: 10px; }
    .phrase-bienvenue { text-align: center; font-family: 'Fredoka One', cursive; color: #5E35B1; font-size: 24px; line-height: 1.2; margin-bottom: 20px; }

    /* BOUTONS GÉANTS */
    .stButton > button { 
        background: white !important; border: 4px solid #9575CD !important; border-radius: 30px !important; 
        color: #5E35B1 !important; font-family: 'Fredoka One', cursive !important; font-size: 20px !important; 
        min-height: 80px !important; width: 100% !important; box-shadow: 0px 6px 0px #D1C4E9 !important; 
        margin-bottom: 10px !important; white-space: normal !important;
    }
    .stButton > button:active { transform: translateY(4px); box-shadow: 0px 2px 0px #D1C4E9 !important; }

    /* ÉCRAN CALCULATRICE (GAUCHE) */
    .calc-screen { 
        background: white; border: 4px solid #9575CD; border-radius: 15px; padding: 15px; 
        text-align: left; font-size: 32px; font-family: 'Fredoka One', cursive; color: #5E35B1; 
        margin-bottom: 15px; min-height: 70px; display: flex; align-items: center;
    }

    /* DÉCO BALLONS */
    .ballon { position: fixed; font-size: 40px; z-index: 0; animation: monte 10s linear infinite; opacity: 0.5; }
    @keyframes monte { 0% { transform: translateY(110vh); } 100% { transform: translateY(-110vh); } }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    <div class="ballon" style="left:5%;">🎈</div>
    <div class="ballon" style="left:85%; animation-delay: 5s%;">🎈</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 6. LOGIQUE DES PAGES ---

# --- PAGE D'ACCUEIL ---
if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='phrase-bienvenue'>Bonjour !<br>Où veux-tu aller <b>pour</b> t'amuser ?</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 ÉCOLE"): st.session_state.mode = "jeu"; st.session_state.slide = 1; st.rerun()
        if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"; st.rerun()
    with c2:
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()
        if st.button("📖 DICO"): st.session_state.mode = "dict"; st.rerun()

# --- MODE ÉCOLE / UNIVERS ---
elif st.session_state.mode == "jeu":
    colh, colb = st.columns(2)
    with colh: 
        if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    with colb:
        if st.session_state.chemin:
            if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    # Barre des Univers
    u1, u2, u3 = st.columns(3)
    if u1.button("🦁 NATURE"): st.session_state.slide, st.session_state.chemin = 2, []
    if u2.button("🌍 MONDE"): st.session_state.slide, st.session_state.chemin = 3, []
    if u3.button("🎁 JEUX"): st.session_state.slide, st.session_state.chemin = 4, []

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: contenu = contenu.get(d, {})

    if isinstance(contenu, dict):
        items = list(contenu.items())
        for i in range(0, len(items), 2):
            ca, cb = st.columns(2)
            with ca:
                k, v = items[i]
                if isinstance(v, dict):
                    if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                else:
                    if st.button(f"🔊 {k}"): parler(v)
            if i + 1 < len(items):
                with cb:
                    k, v = items[i+1]
                    if isinstance(v, dict):
                        if st.button(f"📁 {k}"): st.session_state.chemin.append(k); st.rerun()
                    else:
                        if st.button(f"🔊 {k}"): parler(v)

# --- MODE CALCULATRICE ---
elif st.session_state.mode == "calc":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.session_state.calc_val = ""; st.rerun()
    st.markdown(f"<div class='calc-screen'>{st.session_state.calc_val if st.session_state.calc_val else 'Bonjour !'}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("1"): st.session_state.calc_val += "1"; st.rerun()
        if st.button("4"): st.session_state.calc_val += "4"; st.rerun()
        if st.button("7"): st.session_state.calc_val += "7"; st.rerun()
        if st.button("C"): st.session_state.calc_val = ""; st.rerun()
    with c2:
        if st.button("2"): st.session_state.calc_val += "2"; st.rerun()
        if st.button("5"): st.session_state.calc_val += "5"; st.rerun()
        if st.button("8"): st.session_state.calc_val += "8"; st.rerun()
        if st.button("0"): st.session_state.calc_val += "0"; st.rerun()
    with c3:
        if st.button("3"): st.session_state.calc_val += "3"; st.rerun()
        if st.button("6"): st.session_state.calc_val += "6"; st.rerun()
        if st.button("9"): st.session_state.calc_val += "9"; st.rerun()
        if st.button("="):
            try:
                res = eval(st.session_state.calc_val)
                st.session_state.calc_val = str(res); parler(f"Ça fait {res}")
            except: st.session_state.calc_val = ""; st.rerun()
    with c4:
        if st.button("+"): st.session_state.calc_val += "+"; st.rerun()
        if st.button("-"): st.session_state.calc_val += "-"; st.rerun()
        if st.button("🔊"): parler(st.session_state.calc_val)

# --- MODE DICO (MUET & PUR) ---
elif st.session_state.mode == "dict":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("<h2 style='text-align:center; color:#5E35B1; font-family:Fredoka One;'>📖 LE DICO</h2>", unsafe_allow_html=True)
    m = st.text_input("Écris un mot :")
    if st.button("🌟 VOIR"):
        if m:
            res = ia_magique(m, "dico")
            st.markdown(f"<div style='background:white; border-radius:20px; padding:20px; border:3px solid #9575CD; color:#5E35B1; font-family:Fredoka One; font-size:20px; text-align:center;'>{res}</div>", unsafe_allow_html=True)

# --- MODE DOUDOU IA (PARLE ENFANT) ---
elif st.session_state.mode == "ia":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("<h2 style='text-align:center; color:#5E35B1; font-family:Fredoka One;'>🤖 DOUDOU</h2>", unsafe_allow_html=True)
    q = st.text_input("Dis quelque chose :")
    if st.button("RÉPONDRE"):
        if q:
            res = ia_magique(q, "doudou")
            st.info(res)
            parler(res)
