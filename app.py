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
    st.error("Crée les fichiers dans le dossier /univers !")

# --- 3. DESIGN MOBILE (NÉON ET DOSSIERS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; }
    .titre-titan { text-align: center; color: #00FBFF; font-size: 30px; font-weight: 900; text-shadow: 0 0 10px #00FBFF; }
    
    /* Boutons Dossiers */
    .btn-dossier button {
        background: #111 !important; border: 2px solid #333 !important;
        height: 120px !important; font-size: 22px !important; border-radius: 25px !important;
    }
    
    /* Boutons Objets (dans les dossiers) */
    .btn-objet button {
        background: linear-gradient(135deg, #00FBFF, #0077FF) !important;
        height: 100px !important; font-size: 20px !important; border-radius: 20px !important;
        color: white !important;
    }

    .nav-bar { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ÉTATS DE NAVIGATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'dossier' not in st.session_state: st.session_state.dossier = None

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. BARRE DE NAVIGATION ---
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i] if st.session_state.slide != i+1 else "●", key=f"n_{i}"):
            st.session_state.slide = i+1
            st.session_state.dossier = None # On ferme le dossier quand on change d'univers
            st.rerun()

# --- 6. LOGIQUE D'AFFICHAGE ---
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
data_actuelle = mapping[st.session_state.slide]

st.markdown("<h1 class='titre-titan'>🧠 CERVEAU CENTRAL</h1>", unsafe_allow_html=True)

# SI AUCUN DOSSIER N'EST OUVERT : On affiche les dossiers
if st.session_state.dossier is None:
    st.markdown("<div class='btn-dossier'>", unsafe_allow_html=True)
    for nom_dossier in data_actuelle.keys():
        if st.button(f"📂 {nom_dossier}", key=f"fold_{nom_dossier}"):
            st.session_state.dossier = nom_dossier
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# SI UN DOSSIER EST OUVERT : On affiche le contenu
else:
    if st.button("⬅️ RETOUR", key="back"):
        st.session_state.dossier = None
        st.rerun()
    
    st.subheader(f"Dossier : {st.session_state.dossier}")
    st.markdown("<div class='btn-objet'>", unsafe_allow_html=True)
    
    items = data_actuelle[st.session_state.dossier]
    
    # On affiche les boutons à l'intérieur
    for k, v in (items.items() if isinstance(items, dict) else enumerate(items)):
        label = k if isinstance(items, dict) else v
        audio = v if isinstance(items, dict) else v
        if st.button(label, key=f"item_{label}"):
            parler(audio)
            if "BALLONS" in label.upper(): st.balloons()
            if "MAGIE" in label.upper(): st.snow()
    st.markdown("</div>", unsafe_allow_html=True)
