import streamlit as st
from gtts import gTTS
import base64
import io
import sys
import os

# --- 1. CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="L'EMPIRE", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORTATION DYNAMIQUE ---
# On essaie d'importer les fichiers du dossier /univers
try:
    from univers.ecole import ECOLE_DATA
except:
    ECOLE_DATA = {"Erreur": ["Fichier ecole.py manquant"]}

# --- 3. DESIGN MOBILE "NÉON PUR" ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000000; } 

    /* Titre Cerveau */
    .titre-titan {
        text-align: center; color: #00FBFF; font-size: 35px !important;
        font-weight: 900; letter-spacing: 2px;
        text-shadow: 0 0 15px #00FBFF; margin-bottom: 20px;
    }

    /* Boutons Géants pour Téléphone */
    .stButton > button {
        width: 100% !important; height: 95px !important;
        font-size: 20px !important; font-weight: 800 !important;
        border-radius: 20px !important; border: 2px solid #222 !important;
        background: #111 !important; color: #fff !important;
        margin-bottom: 10px !important; transition: 0.1s;
    }
    
    /* Effet au clic (feedback tactile) */
    .stButton > button:active {
        background: #00FBFF !important; color: #000 !important;
        transform: scale(0.96);
    }

    /* Barre de Navigation (Points) */
    .nav-bar {
        display: flex; justify-content: center; gap: 15px;
        padding: 15px; background: #0A0A0A; border-radius: 40px;
        border: 1px solid #1A1A1A; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MOTEUR AUDIO ---
def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- 5. NAVIGATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1

st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        # Si on est sur le slide, on affiche un point brillant
        label = "●" if st.session_state.slide == i+1 else icons[i]
        if st.button(label, key=f"nav_{i}"):
            st.session_state.slide = i+1
            st.rerun()

# --- 6. AFFICHAGE DES UNIVERS ---
st.markdown("<h1 class='titre-titan'>🧠 CERVEAU CENTRAL</h1>", unsafe_allow_html=True)

if st.session_state.slide == 1:
    # On boucle sur les catégories de ecole.py
    for cat, data in ECOLE_DATA.items():
        st.markdown(f"<h3 style='color:#FF0055; text-align:center; text-shadow: 0 0 10px #FF0055;'>{cat}</h3>", unsafe_allow_html=True)
        # On affiche les items
        for item in data:
            # Si c'est un dictionnaire (ex: Formes)
            if isinstance(data, dict):
                label = f"{item} {data[item]}"
                val_audio = data[item]
            else:
                label = item
                val_audio = item
                
            if st.button(label, key=f"btn_{cat}_{item}"):
                parler(val_audio)
