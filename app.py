import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. IMPORT DES DOSSIERS (Tes fichiers séparés) ---
try:
    import ecole
    import monde
    import nature
    import jeux
except ImportError:
    st.warning("Certains fichiers (.py) sont manquants sur GitHub, mais l'app continue !")

# --- 2. CONFIGURATION ET DESIGN ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* Fond dégradé doux */
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    /* Titre MONDE MAGIQUE en violet foncé */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One'; 
        color: #4A148C !important; 
        font-size: 60px; 
        text-shadow: 2px 2px 0px #FFFFFF;
        margin-bottom: 20px;
    }

    /* BOUTONS ARC-EN-CIEL AVEC TEXTE VIOLET TRÈS FONCÉ */
    .stButton > button { 
        background: white !important; 
        color: #311B92 !important; /* Violet foncé pour bien voir */
        font-family: 'Fredoka One' !important; 
        font-size: 26px !important; 
        font-weight: bold !important;
        min-height: 100px !important; 
        width: 100% !important;
        border: 6px solid !important;
        border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1 !important;
        box-shadow: 0px 8px 0px #D1C4E9 !important;
        margin-bottom: 20px !important;
        border-radius: 15px !important;
    }

    /* Texte des étiquettes et entrées */
    p, span, label { 
        color: #4A148C !important; 
        font-family: 'Fredoka One' !important; 
        font-size: 22px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTIONS UTILES ---
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
        if st.button("🎓 ECOLE"): st.session_state.mode = "ecole"; st.rerun()
        if st.button("🦁 NATURE"): st.session_state.mode = "nature"; st.rerun()
        if st.button("🌍 MONDE"): st.session_state.mode = "monde"; st.rerun()
    with c2:
        if st.button("🎮 JEUX"): st.session_state.mode = "jeux"; st.rerun()
        if st.button("🗣️ PARLEUR"): st.session_state.mode = "parleur"; st.rerun()
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()

# --- VERS LES FICHIERS SÉPARÉS ---
elif st.session_state.mode == "ecole":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try: ecole.afficher() # Ton fichier ecole.py doit avoir une fonction afficher()
    except: st.write("Le fichier ecole.py arrive bientôt !")

elif st.session_state.mode == "nature":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try: nature.afficher()
    except: st.write("Le fichier nature.py arrive bientôt !")

elif st.session_state.mode == "monde":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try: monde.afficher()
    except: st.write("Le fichier monde.py arrive bientôt !")

# --- COIN JEUX (AVEC TON DINO GITHUB) ---
elif st.session_state.mode == "jeux":
    st.markdown("<h1 class='titre-enfant'>🎮 JEUX</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    if st.button("🦖 JEU DU DINO (VRAI JEU)"):
        st.session_state.mode = "jouer_dino"
        st.rerun()

elif st.session_state.mode == "jouer_dino":
    if st.button("⬅️ QUITTER LE JEU"): st.session_state.mode = "jeux"; st.rerun()
    # Lien vers ton fichier dino.html sur GitHub
    url_dino = "https://zachariepays-debug.github.io/jeux-magiques/dino.html"
    st.components.v1.iframe(url_dino, height=600, scrolling=False)

# --- OUTILS ---
elif st.session_state.mode == "parleur":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("### 🗣️ Écris quelque chose et je le dirai !")
    phrase = st.text_area("Ta phrase :", height=100)
    if st.button("🔊 PARLER MAINTENANT"): parler(phrase)

elif st.session_state.mode == "calc":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.write("### 🧮 Ma Calculatrice Magique")
    # Code simplifié de calculatrice
    n1 = st.number_input("Premier nombre", value=0)
    op = st.selectbox("Action", ["+", "-", "x"])
    n2 = st.number_input("Deuxième nombre", value=0)
    if st.button("CALCULER"):
        res = n1 + n2 if op=="+" else n1 - n2 if op=="-" else n1 * n2
        st.success(f"Le résultat est {res}")
        parler(f"Ça fait {res}")
