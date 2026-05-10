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
except:
    st.error("Dossier /univers introuvable !")

# --- 3. DESIGN "EASY-CLICK" (ÉPURE ET GÉANT) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    
    /* Titre très clair */
    .titre-enfant { 
        text-align: center; color: white; font-size: 28px; 
        font-weight: 900; margin-bottom: 20px;
    }
    
    /* BOUTONS DOSSIERS (Gris foncés, très larges) */
    div[data-testid="stVerticalBlock"] > div .btn-dossier button {
        background-color: #1A1A1A !important;
        border: 4px solid #333 !important;
        height: 120px !important;
        font-size: 26px !important;
        border-radius: 30px !important;
        color: #00FBFF !important;
    }
    
    /* BOUTONS OBJETS (Couleurs vives pour l'action) */
    div[data-testid="stVerticalBlock"] > div .btn-objet button {
        background: linear-gradient(180deg, #00FBFF, #0077FF) !important;
        height: 110px !important;
        font-size: 24px !important;
        border-radius: 25px !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 6px #004488;
    }
    
    /* BOUTON RETOUR (Indispensable et énorme) */
    .btn-retour button {
        background-color: #FF0055 !important;
        height: 70px !important;
        font-size: 20px !important;
        border-radius: 50px !important;
        color: white !important;
        margin-bottom: 20px !important;
    }

    /* Barre de navigation simplifiée */
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

# --- 5. ÉTATS ET NAVIGATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'dossier' not in st.session_state: st.session_state.dossier = None

# Barre du haut (4 gros choix)
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i] if st.session_state.slide != i+1 else "●", key=f"n_{i}"):
            st.session_state.slide = i+1
            st.session_state.dossier = None
            st.rerun()

# --- 6. AFFICHAGE ---
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
data_actuelle = mapping[st.session_state.slide]

# ÉCRAN 1 : CHOIX DU DOSSIER
if st.session_state.dossier is None:
    st.markdown("<h1 class='titre-enfant'>CHOISIS UN DOSSIER</h1>", unsafe_allow_html=True)
    for nom_dossier in data_actuelle.keys():
        st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
        if st.button(f"📂 {nom_dossier}", key=f"f_{nom_dossier}"):
            st.session_state.dossier = nom_dossier
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ÉCRAN 2 : CONTENU DU DOSSIER
else:
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    if st.button("⬅️ RETOUR", key="back"):
        st.session_state.dossier = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='titre-enfant'>{st.session_state.dossier}</h1>", unsafe_allow_html=True)
    
    items = data_actuelle[st.session_state.dossier]
    
    for k, v in (items.items() if isinstance(items, dict) else enumerate(items)):
        label = k if isinstance(items, dict) else v
        audio = v if isinstance(items, dict) else v
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(label, key=f"i_{label}"):
            parler(audio)
            if "BALLONS" in label.upper(): st.balloons()
            if "MAGIE" in label.upper(): st.snow()
        st.markdown('</div>', unsafe_allow_html=True)
