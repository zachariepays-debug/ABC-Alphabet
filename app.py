import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MON SUPER JOUET", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORTATION DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    st.error("Oups ! Les dossiers sont perdus !")

# --- 3. DESIGN "BÉBÉ FLASHY" ---
st.markdown("""
    <style>
    /* Fond dégradé super joyeux */
    .stApp { 
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); 
    }
    
    .titre-enfant { 
        text-align: center; 
        color: #FF00FF; 
        font-size: 40px; 
        font-weight: 900; 
        text-shadow: 3px 3px 0px #FFF, 5px 5px 0px #00FBFF;
        margin-bottom: 20px;
        font-family: 'Comic Sans MS', cursive;
    }
    
    /* Boutons de navigation (Icones du haut) */
    .stButton > button {
        transition: transform 0.2s;
    }
    .stButton > button:active {
        transform: scale(0.9);
    }

    /* Dossiers (Gros boutons ronds jaunes) */
    .btn-dossier button {
        background: #FFEB3B !important; 
        border: 6px solid #FF9800 !important;
        height: 120px !important; 
        font-size: 26px !important; 
        border-radius: 40px !important;
        color: #E91E63 !important; 
        margin-bottom: 15px !important;
        box-shadow: 0px 8px 0px #FB8C00 !important;
    }
    
    /* Objets (Boutons Arc-en-ciel qui flashent) */
    .btn-objet:nth-child(4n+1) button { background: #FF4081 !important; border: 5px solid #F50057 !important; box-shadow: 0px 8px 0px #C51162 !important; }
    .btn-objet:nth-child(4n+2) button { background: #00E676 !important; border: 5px solid #00C853 !important; box-shadow: 0px 8px 0px #1B5E20 !important; }
    .btn-objet:nth-child(4n+3) button { background: #00B0FF !important; border: 5px solid #0091EA !important; box-shadow: 0px 8px 0px #01579B !important; }
    .btn-objet:nth-child(4n+4) button { background: #AA00FF !important; border: 5px solid #D500F9 !important; box-shadow: 0px 8px 0px #4A148C !important; }

    .btn-objet button {
        height: 110px !important; 
        font-size: 28px !important; 
        border-radius: 35px !important;
        color: white !important; 
        margin-bottom: 15px !important;
        font-weight: bold !important;
    }

    /* Bouton RETOUR (Gros bouton orange) */
    .btn-retour button {
        background: #FF6D00 !important; 
        color: white !important;
        height: 70px !important; 
        border-radius: 60px !important;
        font-size: 22px !important;
        border: 4px solid #FFF !important;
    }
    
    .nav-bar { background: white; padding: 10px; border-radius: 50px; display: flex; justify-content: center; gap: 10px; box-shadow: 0px 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE AUDIO ---
def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. ÉTATS ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Navigation du haut
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i], key=f"n_{i}"):
            st.session_state.slide = i+1
            st.session_state.chemin = []
            st.rerun()

# Données
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping[st.session_state.slide]
for dossier in st.session_state.chemin:
    contenu = contenu[dossier]

# Affichage
if len(st.session_state.chemin) > 0:
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    if st.button("⬅️ ON REVIENT !", key="back"):
        st.session_state.chemin.pop()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<h1 class='titre-enfant'>{'⭐ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'CHOISIS TON JEU !'}</h1>", unsafe_allow_html=True)

# Boutons Grid
if isinstance(contenu, dict):
    for nom, valeur in contenu.items():
        if isinstance(valeur, (dict, list)) and not isinstance(valeur, str):
            st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
            if st.button(f"📂 {nom}", key=f"d_{nom}"):
                st.session_state.chemin.append(nom)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
            if st.button(nom, key=f"i_{nom}"):
                parler(valeur)
            st.markdown('</div>', unsafe_allow_html=True)
elif isinstance(contenu, list):
    for item in contenu:
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(str(item), key=f"l_{item}"):
            parler(item)
        st.markdown('</div>', unsafe_allow_html=True)
