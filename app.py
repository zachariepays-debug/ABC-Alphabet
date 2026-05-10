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
    if not MISTRAL_API_KEY: return "Clé magique ?"
    system_instruction = "Tu es un doudou gentil. Phrases très courtes."
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": "mistral-tiny", "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": f"Mode={mode}. {prompt}"}]}
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except: return "Le doudou dort..."

# --- 4. DESIGN "ZERO SCROLL" (TOUT SUR UNE PAGE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp { background: linear-gradient(135deg, #E0F7FA 0%, #F3E5F5 50%, #FFF9C4 100%); }

    /* Réduction drastique des marges Streamlit */
    .block-container {
        padding-top: 10px !important;
        padding-bottom: 0px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        max-width: 100%;
    }

    /* TITRE COMPACT */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One', cursive !important;
        color: #9575CD !important; 
        font-size: 28px !important;
        margin-bottom: 5px !important;
        text-shadow: 1px 1px 0px white;
    }

    /* FORCE LES BOUTONS EN 2 COLONNES SUR MOBILE */
    [data-testid="column"] {
        width: 48% !important;
        flex: 1 1 45% !important;
        min-width: 45% !important;
        display: inline-block !important;
        margin: 1% !important;
    }

    /* STYLE DES BOUTONS PLUS PETITS */
    .stButton > button { 
        background: white !important; 
        border: 3px solid #9575CD !important; 
        border-radius: 20px !important; 
        color: #5E35B1 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 14px !important; 
        height: 50px !important; /* Hauteur réduite pour tout voir */
        width: 100% !important; 
        box-shadow: 0px 3px 0px #D1C4E9 !important; 
        padding: 0px !important;
    }

    /* BALLON DÉCORATIF FIXE */
    .ballon { position: fixed; bottom: 10px; right: 10px; font-size: 30px; z-index: 10; }
    
    /* Cache les éléments inutiles de Streamlit sur mobile */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    <div class="ballon">🎈</div>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. NAVIGATION COMPACTE (2x2) ---
c1, c2 = st.columns(2)
with c1: 
    if st.button("📚 ECOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
    if st.button("📖 DICO"): st.session_state.mode = "dict"
with c2: 
    if st.button("🧮 CALC"): st.session_state.mode = "calc"
    if st.button("🤖 IA"): st.session_state.mode = "ia"

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# --- BOUTONS DES UNIVERS (Ligne de 3) ---
u1, u2, u3 = st.columns(3)
# On force le style pour que ces 3 là soient sur la même ligne
st.markdown("<style>[data-testid='stHorizontalBlock'] div { width: 33% !important; }</style>", unsafe_allow_html=True)

if u1.button("🦁 NAT"): st.session_state.slide, st.session_state.chemin = 2, []
if u2.button("🌍 MON"): st.session_state.slide, st.session_state.chemin = 3, []
if u3.button("🎁 JEU"): st.session_state.slide, st.session_state.chemin = 4, []

# --- CONTENU DYNAMIQUE ---
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping.get(st.session_state.slide, {})
for d in st.session_state.chemin: contenu = contenu.get(d, {})

if st.session_state.chemin:
    if st.button("⬅️ RETOUR"): st.session_state.chemin.pop(); st.rerun()

# Affichage en grille de 2 colonnes pour les dossiers/objets
if isinstance(contenu, dict):
    # On crée des colonnes dynamiques pour éviter l'effet "liste infinie"
    grid_cols = st.columns(2)
    for idx, (k, v) in enumerate(contenu.items()):
        target_col = grid_cols[idx % 2]
        with target_col:
            if isinstance(v, dict):
                if st.button(f"📁 {k}"): 
                    st.session_state.chemin.append(k)
                    st.rerun()
            else:
                if st.button(f"🔊 {k}"): parler(v)
