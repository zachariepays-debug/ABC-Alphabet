import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. INITIALISATION ---
if 'mode' not in st.session_state: st.session_state.mode = "accueil"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []
if 'calc_val' not in st.session_state: st.session_state.calc_val = ""

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
    # Au cas où les fichiers sont absents, on crée des dictionnaires vides
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 4. LOGIQUE IA ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY: return "Clé magique ?"
    system = "Tu es un dictionnaire enfantin. Donne UNIQUEMENT la définition courte." if mode == "dico" else "Tu es Doudou, un ourson mimi."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Oups..."

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
    .calc-screen { background: white; border: 4px solid #5E35B1; border-radius: 15px; padding: 15px; text-align: left; font-size: 40px; color: #5E35B1; margin-bottom: 10px; min-height: 70px; }
    </style>
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
    c1, c2 = st.columns(2)
    with c1:
        # LE NOUVEAU BOUTON QUI REGROUPE TOUT
        if st.button("🎓 APPRENTISSAGE"): 
            st.session_state.mode = "jeu"
            st.session_state.slide = 1 # On commence par l'écran de choix (Ecole, Nature, etc.)
            st.session_state.chemin = []
            st.rerun()
        if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"; st.rerun()
    with c2:
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()
        if st.button("📖 DICO"): st.session_state.mode = "dict"; st.rerun()

elif st.session_state.mode == "jeu":
    # NAVIGATION HAUT
    col_nav1, col_nav2 = st.columns([1,1])
    with col_nav1:
        if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    with col_nav2:
        if st.session_state.chemin:
            if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

    # CHOIX DE L'UNIVERS (Seulement si on n'est pas encore rentré dans un dossier)
    if not st.session_state.chemin:
        st.markdown("<h3 style='text-align:center; color:#5E35B1;'>Que veux-tu apprendre ?</h3>", unsafe_allow_html=True)
        u1, u2 = st.columns(2)
        with u1:
            if st.button("🏫 L'ÉCOLE"): st.session_state.slide = 1; st.session_state.chemin = ["ECOLE"]; st.rerun()
            if st.button("🦁 LA NATURE"): st.session_state.slide = 2; st.session_state.chemin = ["NATURE"]; st.rerun()
        with u2:
            if st.button("🌍 LE MONDE"): st.session_state.slide = 3; st.session_state.chemin = ["MONDE"]; st.rerun()
            if st.button("🎁 LES JEUX"): st.session_state.slide = 4; st.session_state.chemin = ["JEUX"]; st.rerun()

    # LOGIQUE DE RÉCUPÉRATION DES DONNÉES
    # On crée un dictionnaire maître pour la navigation
    MASTER_DATA = {
        "ECOLE": ECOLE_DATA,
        "NATURE": NATURE_DATA,
        "MONDE": MONDE_DATA,
        "JEUX": JEUX_DATA
    }
    
    contenu = MASTER_DATA
    for d in st.session_state.chemin:
        if isinstance(contenu, dict):
            contenu = contenu.get(d, {})

    # AFFICHAGE DES DOSSIERS ET SONS
    if isinstance(contenu, dict) and st.session_state.chemin:
        items = list(contenu.items())
        for i in range(0, len(items), 2):
            ca, cb = st.columns(2)
            with ca:
                k, v = items[i]
                type_icon = "📁" if isinstance(v, dict) else "🔊"
                if st.button(f"{type_icon} {k}"):
                    if isinstance(v, dict): st.session_state.chemin.append(k); st.rerun()
                    else: parler(v)
            if i + 1 < len(items):
                with cb:
                    k, v = items[i+1]
                    type_icon = "📁" if isinstance(v, dict) else "🔊"
                    if st.button(f"{type_icon} {k}"):
                        if isinstance(v, dict): st.session_state.chemin.append(k); st.rerun()
                        else: parler(v)

# --- LES MODES CALCULS / DICO / IA RESTENT LES MÊMES (OPTIMISÉS MOBILE) ---
elif st.session_state.mode == "calc":
    if st.button("🏠 QUITTER"): st.session_state.mode = "accueil"; st.session_state.calc_val = ""; st.rerun()
    st.markdown(f"<div class='calc-screen'>{st.session_state.calc_val if st.session_state.calc_val else '0'}</div>", unsafe_allow_html=True)
    
    # Input invisible pour clavier téléphone
    st.text_input("Clavier téléphone :", key="phone_input", on_change=lambda: st.session_state.update(calc_val=st.session_state.phone_input))

    c1, c2, c3 = st.columns(3)
    btns = [("1","2","3"), ("4","5","6"), ("7","8","9"), ("+","0","-")]
    for row in btns:
        with c1: 
            if st.button(row[0]): st.session_state.calc_val += row[0]; st.rerun()
        with c2: 
            if st.button(row[1]): st.session_state.calc_val += row[1]; st.rerun()
        with c3: 
            if st.button(row[2]): st.session_state.calc_val += row[2]; st.rerun()
    
    ca, cb = st.columns(2)
    if ca.button("🗑️ EFFACER"): st.session_state.calc_val = ""; st.rerun()
    if cb.button("⭐ ÉGAL"):
        try:
            res = eval(st.session_state.calc_val)
            st.session_state.calc_val = str(res); parler(f"Ça fait {res}")
        except: st.session_state.calc_val = ""; st.rerun()

elif st.session_state.mode == "dict":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    m = st.text_input("Mot :")
    if st.button("🌟 VOIR"):
        if m: res = ia_magique(m, "dico"); st.write(f"### {res}"); parler(res)

elif st.session_state.mode == "ia":
    if st.button("🏠 ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    q = st.text_input("Dis à Doudou :")
    if st.button("RÉPONDRE"):
        if q: res = ia_magique(q, "doudou"); st.info(res); parler(res)
