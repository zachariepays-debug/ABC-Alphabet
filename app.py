import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Génies", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORTATIONS DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
    UNIVERS = [ECOLE_DATA, NATURE_DATA, MONDE_DATA, JEUX_DATA]
except Exception as e:
    st.error("Assure-toi que le dossier 'univers' contient bien les 4 fichiers .py")
    UNIVERS = [{}, {}, {}, {}]

# --- 3. DESIGN "CLEAN MOBILE" ---
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { background-color: #000; }
    
    /* Titre Minimaliste */
    .titre-simple {
        text-align: center; color: white; font-size: 28px !important;
        font-weight: 700; margin-bottom: 20px; letter-spacing: 1px;
    }

    /* Boutons de Navigation (Cercles) */
    .nav-box { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
    
    /* Boutons de Contenu (Massifs) */
    .stButton > button {
        width: 100% !important; height: 90px !important;
        font-size: 20px !important; font-weight: 800 !important;
        border-radius: 20px !important; border: none !important;
        background: #1A1A1A !important; color: white !important;
        margin-bottom: 10px !important;
    }
    
    /* Couleurs de sélection */
    .btn-active button { background: #00FBFF !important; color: black !important; border: 2px solid white !important; }
    
    .stButton > button:active { transform: scale(0.95); background: white !important; color: black !important; }
    
    h3 { color: #555; text-transform: uppercase; font-size: 14px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUDIO ---
def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- 5. LOGIQUE ---
if 'slide' not in st.session_state: st.session_state.slide = 1

st.markdown("<div class='titre-simple'>L'EMPIRE DES GÉNIES</div>", unsafe_allow_html=True)

# Navigation
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        is_active = st.session_state.slide == i+1
        if is_active:
            st.markdown("<div class='btn-active'>", unsafe_allow_html=True)
        if st.button(icons[i], key=f"nav_{i}"):
            st.session_state.slide = i+1
            st.rerun()
        if is_active:
            st.markdown("</div>", unsafe_allow_html=True)

# Affichage des données
data_actuelle = UNIVERS[st.session_state.slide - 1]

for section, items in data_actuelle.items():
    st.markdown(f"<h3>{section}</h3>", unsafe_allow_html=True)
    
    # Gestion automatique Liste ou Dictionnaire
    if isinstance(items, list):
        for item in items:
            if st.button(item, key=f"btn_{item}"):
                parler(item)
    else:
        for k, v in items.items():
            if st.button(k, key=f"btn_{k}"):
                parler(v)
                # Effets spéciaux pour le slide JEUX
                if "CADEAU" in k or "MAGIE" in k: st.snow()
                if "BALLONS" in k or "FÊTE" in k: st.balloons()
