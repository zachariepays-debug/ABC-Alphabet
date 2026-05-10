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

# --- 2. CONFIGURATION PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide")

# --- 3. DESIGN ARC-EN-CIEL ET VISIBILITÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* Fond dégradé */
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    /* Titre bien visible */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One'; 
        color: #5E35B1 !important; 
        font-size: 50px; 
        text-shadow: 3px 3px 0px #FFFFFF;
        margin-bottom: 30px;
    }

    /* BOUTONS AVEC TEXTE FONCÉ ET BORDURE ARC-EN-CIEL */
    .stButton > button { 
        background: white !important; 
        color: #4A148C !important; /* Violet très foncé pour bien lire */
        font-family: 'Fredoka One' !important; 
        font-size: 22px !important; 
        min-height: 90px !important; 
        width: 100% !important;
        border: 6px solid !important;
        border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1 !important;
        border-radius: 20px !important; /* Note: border-image peut annuler le radius sur certains navigateurs */
        box-shadow: 0px 6px 0px #D1C4E9 !important;
        margin-bottom: 15px !important;
    }

    /* Forcer la couleur du texte dans les zones de saisie */
    input, textarea {
        color: #4A148C !important;
        font-weight: bold !important;
    }
    
    /* Style pour les petits textes de consignes */
    p, span, label {
        color: #311B92 !important;
        font-family: 'Fredoka One', sans-serif !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    if txt:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 4. NAVIGATION ---

if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>🎈 MONDE MAGIQUE 🎈</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎓 APPRENTISSAGE"): st.session_state.mode, st.session_state.chemin = "jeu", []; st.rerun()
        if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"; st.rerun()
        if st.button("🗣️ MACHINE À PHRASES"): st.session_state.mode = "parleur"; st.rerun()
    with c2:
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()
        if st.button("📖 DICO"): st.session_state.mode = "dict"; st.rerun()
        if st.button("🎮 JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()

# Les autres sections (Calculs, Jeux, etc.) utilisent maintenant ces nouveaux styles automatiquement.

elif st.session_state.mode == "menu_jeux":
    st.markdown("<h1 class='titre-enfant'>🎮 COIN JEUX</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    cj1, cj2 = st.columns(2)
    if cj1.button("🦖 DINO SAUTEUR"): st.session_state.mode = "dino"; st.rerun()
    if cj1.button("🎈 MONTGOLFIÈRE"): st.session_state.mode = "balon"; st.rerun()
    if cj2.button("🔢 CHIFFRE CACHÉ"): st.session_state.mode = "cache"; st.rerun()
