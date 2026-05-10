import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide")

# --- 2. LE DESIGN MAGIQUE (Violet Foncé & Arc-en-ciel) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    .titre-enfant { 
        text-align: center; font-family: 'Fredoka One'; color: #4A148C !important; 
        font-size: 60px; text-shadow: 2px 2px 0px #FFFFFF; margin-bottom: 20px;
    }

    .stButton > button { 
        background: white !important; color: #311B92 !important; /* TEXTE BIEN FONCÉ */
        font-family: 'Fredoka One' !important; font-size: 26px !important; 
        min-height: 100px !important; width: 100% !important;
        border: 6px solid !important;
        border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1 !important;
        box-shadow: 0px 8px 0px #D1C4E9 !important;
        margin-bottom: 20px !important;
    }

    p, span, label { color: #4A148C !important; font-family: 'Fredoka One' !important; font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTION VOIX ---
def parler(txt):
    if txt:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if 'mode' not in st.session_state:
    st.session_state.mode = "accueil"

# PAGE D'ACCUEIL
if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>🎈 MONDE MAGIQUE 🎈</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏫 ECOLE"): st.session_state.mode = "ecole"; st.rerun()
        if st.button("🦁 NATURE"): st.session_state.mode = "nature"; st.rerun()
    with c2:
        if st.button("🎮 JEUX"): st.session_state.mode = "jeux"; st.rerun()
        if st.button("🗣️ PARLEUR"): st.session_state.mode = "parleur"; st.rerun()

# --- SECTION ECOLE ---
elif st.session_state.mode == "ecole":
    st.markdown("<h1 class='titre-enfant'>🏫 L'ÉCOLE</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    col1, col2 = st.columns(2)
    if col1.button("🍎 LES FRUITS"): parler("La pomme, la banane et l'orange.")
    if col2.button("🔢 COMPTER"): parler("Un, deux, trois, quatre, cinq !")

# --- SECTION NATURE ---
elif st.session_state.mode == "nature":
    st.markdown("<h1 class='titre-enfant'>🦁 LA NATURE</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    if st.button("🦁 LE LION"): parler("Le lion est le roi de la savane. Il fait grrrr !")

# --- SECTION JEUX ---
elif st.session_state.mode == "jeux":
    st.markdown("<h1 class='titre-enfant'>🎮 JEUX</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    if st.button("🦖 JEU DU DINO"):
        st.write("Le jeu va s'afficher ici !")

# --- SECTION PARLEUR ---
elif st.session_state.mode == "parleur":
    st.markdown("<h1 class='titre-enfant'>🗣️ MACHINE À PARLER</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    texte = st.text_area("Écris ici ce que je dois dire :")
    if st.button("🔊 PARLER"):
        parler(texte)
