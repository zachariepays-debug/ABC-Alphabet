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

# --- 3. DESIGN MOBILE ---
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

# --- 5. ÉTATS DE NAVIGATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1
# On utilise une liste pour suivre le chemin (ex: ["LES MATHS", "TABLES"])
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Barre du haut
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i] if st.session_state.slide != i+1 else "●", key=f"n_{i}"):
            st.session_state.slide = i+1
            st.session_state.chemin = [] # On revient à la racine
            st.rerun()

# --- 6. RÉCUPÉRATION DES DONNÉES ---
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping[st.session_state.slide]

# On descend dans le dictionnaire selon le chemin parcouru
for dossier in st.session_state.chemin:
    contenu = contenu[dossier]

# --- 7. AFFICHAGE DYNAMIQUE ---
if len(st.session_state.chemin) > 0:
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    if st.button("⬅️ RETOUR", key="back"):
        st.session_state.chemin.pop() # On remonte d'un niveau
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<h1 class='titre-enfant'>{' > '.join(st.session_state.chemin) if st.session_state.chemin else 'CHOISIS UN DOSSIER'}</h1>", unsafe_allow_html=True)

# On vérifie si ce qu'on affiche est encore un dossier ou une liste d'objets
if isinstance(contenu, dict):
    # C'est un dossier (ou sous-dossier)
    for nom, valeur in contenu.items():
        if isinstance(valeur, (dict, list)) and not isinstance(valeur, str):
            # C'est encore un dossier
            st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
            if st.button(f"📂 {nom}", key=f"d_{nom}"):
                st.session_state.chemin.append(nom)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # C'est un objet final dans un dictionnaire
            st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
            if st.button(nom, key=f"i_{nom}"):
                parler(valeur)
            st.markdown('</div>', unsafe_allow_html=True)
            
elif isinstance(contenu, list):
    # C'est une liste d'objets (comme les chiffres)
    for item in contenu:
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(str(item), key=f"l_{item}"):
            parler(item)
        st.markdown('</div>', unsafe_allow_html=True)
