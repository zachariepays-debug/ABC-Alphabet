import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. IMPORTATION DE TES DOSSIERS ---
# On essaie de charger tes fichiers. S'ils ne sont pas parfaits, l'app ne plante pas.
try:
    import ecole
    import monde
    import nature
    import jeux
except Exception as e:
    pass

# --- 2. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide")

# --- 3. LE DESIGN (Arc-en-ciel + Violet Foncé) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* Fond dégradé */
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    /* Titre Principal */
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One'; 
        color: #4A148C !important; 
        font-size: 60px; 
        text-shadow: 2px 2px 0px #FFFFFF;
        margin-bottom: 20px;
    }

    /* BOUTONS AVEC BORDURE ARC-EN-CIEL ET TEXTE TRÈS LISIBLE */
    .stButton > button { 
        background: white !important; 
        color: #311B92 !important; /* Violet Foncé */
        font-family: 'Fredoka One' !important; 
        font-size: 26px !important; 
        font-weight: bold !important;
        min-height: 100px !important; 
        width: 100% !important;
        border: 6px solid !important;
        border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1 !important;
        box-shadow: 0px 8px 0px #D1C4E9 !important;
        margin-bottom: 20px !important;
    }

    /* Style pour les textes et les bulles d'info */
    p, span, label, .stAlert { 
        color: #4A148C !important; 
        font-family: 'Fredoka One' !important; 
        font-size: 22px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FONCTION POUR PARLER ---
def parler(txt):
    if txt:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. SYSTÈME DE NAVIGATION ---
if 'mode' not in st.session_state:
    st.session_state.mode = "accueil"

# PAGE D'ACCUEIL
if st.session_state.mode == "accueil":
    st.markdown("<h1 class='titre-enfant'>🎈 MONDE MAGIQUE 🎈</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏫 ECOLE"): st.session_state.mode = "ecole"; st.rerun()
        if st.button("🦁 NATURE"): st.session_state.mode = "nature"; st.rerun()
        if st.button("🌍 MONDE"): st.session_state.mode = "monde"; st.rerun()
    with c2:
        if st.button("🎮 JEUX"): st.session_state.mode = "jeux"; st.rerun()
        if st.button("🗣️ PARLEUR"): st.session_state.mode = "parleur"; st.rerun()
        if st.button("🧮 CALCULS"): st.session_state.mode = "calc"; st.rerun()

# --- CONNEXION AUX FICHIERS GITHUB ---

elif st.session_state.mode == "ecole":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try:
        ecole.afficher() # Exécute le code dans ecole.py
    except:
        st.error("Erreur : Vérifie que ecole.py contient bien 'def afficher():'")

elif st.session_state.mode == "nature":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try:
        nature.afficher()
    except:
        st.error("Erreur : Vérifie que nature.py contient bien 'def afficher():'")

elif st.session_state.mode == "monde":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    try:
        monde.afficher()
    except:
        st.error("Erreur : Vérifie que monde.py contient bien 'def afficher():'")

# --- SECTION JEUX (DINO) ---
elif st.session_state.mode == "jeux":
    st.markdown("<h1 class='titre-enfant'>🎮 COIN JEUX</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    
    if st.button("🦖 JEU DU DINOSAURE"):
        st.session_state.mode = "jouer_dino"
        st.rerun()

elif st.session_state.mode == "jouer_dino":
    if st.button("⬅️ QUITTER LE JEU"): st.session_state.mode = "jeux"; st.rerun()
    # Lien vers ton jeu sur GitHub
    url_dino = "https://zachariepays-debug.github.io/jeux-magiques/dino.html"
    st.components.v1.iframe(url_dino, height=600, scrolling=False)

# --- OUTILS SUPPLÉMENTAIRES ---
elif st.session_state.mode == "parleur":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("### 🗣️ Machine à parler")
    phrase = st.text_area("Écris ici :")
    if st.button("🔊 PARLER"): parler(phrase)

elif st.session_state.mode == "calc":
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    st.markdown("### 🧮 Calculatrice")
    n1 = st.number_input("Nombre 1", value=0)
    n2 = st.number_input("Nombre 2", value=0)
    if st.button("ADDITION"):
        res = n1 + n2
        st.success(f"Résultat : {res}")
        parler(f"Ça fait {res}")
