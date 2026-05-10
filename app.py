import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="L'EMPIRE", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORTATION DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except Exception as e:
    st.error(f"Erreur d'importation : {e}")

# --- 3. DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    .titre-enfant { text-align: center; color: white; font-size: 26px; font-weight: 900; margin-bottom: 20px; }
    .btn-dossier button {
        background-color: #1A1A1A !important; border: 4px solid #333 !important;
        height: 100px !important; font-size: 22px !important; border-radius: 25px !important;
        color: #00FBFF !important; margin-bottom: 10px !important; width: 100% !important;
    }
    .btn-objet button {
        background: linear-gradient(180deg, #00FBFF, #0077FF) !important;
        height: 90px !important; font-size: 22px !important; border-radius: 20px !important;
        color: white !important; border: none !important; margin-bottom: 10px !important; width: 100% !important;
    }
    .btn-retour button {
        background-color: #FF0055 !important; height: 60px !important;
        font-size: 18px !important; border-radius: 50px !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- 4. NAVIGATION SÉCURISÉE ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Barre de navigation du haut
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i] if st.session_state.slide != i+1 else "●", key=f"nav_{i}"):
            st.session_state.slide = i+1
            st.session_state.chemin = []
            st.rerun()

# --- 5. CHARGEMENT DES DONNÉES ---
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping.get(st.session_state.slide, ECOLE_DATA)

# SÉCURITÉ : On vérifie que le chemin existe toujours
nouveau_chemin = []
for dossier in st.session_state.chemin:
    if isinstance(contenu, dict) and dossier in contenu:
        contenu = contenu[dossier]
        nouveau_chemin.append(dossier)
    else:
        # Si le dossier n'existe plus, on arrête de descendre
        break
st.session_state.chemin = nouveau_chemin

# --- 6. AFFICHAGE ---
if st.session_state.chemin:
    if st.button("⬅️ RETOUR", key="back"):
        st.session_state.chemin.pop()
        st.rerun()

titre = " > ".join(st.session_state.chemin) if st.session_state.chemin else "CHOISIS UN DOSSIER"
st.markdown(f"<h1 class='titre-enfant'>{titre}</h1>", unsafe_allow_html=True)

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
            if st.button(nom, key=f"obj_{nom}"):
                parler(valeur)
            st.markdown('</div>', unsafe_allow_html=True)
elif isinstance(contenu, list):
    for item in contenu:
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(str(item), key=f"li_{item}"):
            parler(item)
        st.markdown('</div>', unsafe_allow_html=True)
