import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="L'EMPIRE", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORTATION DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except Exception as e:
    st.error(f"Erreur d'importation des dossiers : {e}")

# --- 3. DESIGN ARC-EN-CIEL ET INTERFACE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    .titre-enfant { 
        text-align: center; color: #FF00FF; font-size: 35px; 
        font-weight: 900; text-shadow: 3px 3px #00FBFF; margin-bottom: 20px; 
    }
    
    /* Style des Dossiers (Gris et Néon) */
    .btn-dossier button {
        background-color: #1A1A1A !important; border: 4px solid #444 !important;
        height: 110px !important; font-size: 24px !important; border-radius: 30px !important;
        color: #00FBFF !important; margin-bottom: 12px !important; width: 100% !important;
        font-weight: bold !important;
    }
    
    /* Style des Objets (Boutons qui parlent) - Couleurs Flashy */
    .btn-objet button {
        height: 100px !important; font-size: 24px !important; border-radius: 25px !important;
        color: white !important; border: 3px solid rgba(255,255,255,0.2) !important;
        margin-bottom: 12px !important; font-weight: bold !important; width: 100% !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3) !important;
    }

    /* Couleurs alternées pour les boutons objets */
    div[data-testid="stVerticalBlock"] > div:nth-child(5n+1) .btn-objet button { background: linear-gradient(135deg, #FF0055, #FF5500) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5n+2) .btn-objet button { background: linear-gradient(135deg, #00FBFF, #0077FF) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5n+3) .btn-objet button { background: linear-gradient(135deg, #AA00FF, #FF00FF) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5n+4) .btn-objet button { background: linear-gradient(135deg, #00FF00, #008800) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5n+5) .btn-objet button { background: linear-gradient(135deg, #FFD700, #FF8C00) !important; }

    /* Bouton Retour */
    .btn-retour button { 
        background-color: #FF0055 !important; color: white !important; 
        border-radius: 50px !important; font-weight: 900 !important; width: 100% !important;
    }
    
    .nav-bar { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE AUDIO ---
def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. GESTION DE LA NAVIGATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Barre de navigation supérieure
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚 ÉCOLE", "🦁 NATURE", "🌍 MONDE", "🎁 JEUX"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i], key=f"nav_{i}"):
            st.session_state.slide = i + 1
            st.session_state.chemin = [] # Reset du chemin quand on change d'univers
            st.rerun()

# Sélection des données selon l'univers
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping[st.session_state.slide]

# On descend dans les dossiers selon le chemin
for dossier in st.session_state.chemin:
    if isinstance(contenu, dict) and dossier in contenu:
        contenu = contenu[dossier]

# --- 6. AFFICHAGE DES BOUTONS ---

# Bouton Retour (si on est dans un sous-dossier)
if len(st.session_state.chemin) > 0:
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    if st.button("⬅️ RETOUR", key="back_btn"):
        st.session_state.chemin.pop()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Titre de la section
titre = st.session_state.chemin[-1] if st.session_state.chemin else icons[st.session_state.slide-1]
st.markdown(f"<div class='titre-enfant'>{titre}</div>", unsafe_allow_html=True)

# Grille de boutons
if isinstance(contenu, dict):
    for nom, valeur in contenu.items():
        if isinstance(valeur, (dict, list)) and not isinstance(valeur, str):
            # C'est un DOSSIER
            st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
            if st.button(f"{nom}", key=f"doss_{nom}"):
                st.session_state.chemin.append(nom)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # C'est un OBJET (il parle)
            st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
            if st.button(f"{nom}", key=f"obj_{nom}"):
                parler(valeur)
            st.markdown('</div>', unsafe_allow_html=True)

elif isinstance(contenu, list):
    for item in contenu:
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(f"{item}", key=f"list_{item}"):
            parler(item)
        st.markdown('</div>', unsafe_allow_html=True)
