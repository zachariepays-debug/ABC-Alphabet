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

# --- 3. LES DONNÉES DES DOSSIERS (POUR QU'ILS NE SOIENT PAS VIDES) ---
ECOLE_DATA = {
    "Les Couleurs": {"Rouge": "Le rouge comme une pomme.", "Bleu": "Le bleu comme le ciel.", "Vert": "Le vert comme l'herbe."},
    "Les Chiffres": {"1": "Le chiffre Un", "2": "Le chiffre Deux", "3": "Le chiffre Trois"},
    "L'Alphabet": {"A": "A comme Avion", "B": "B comme Ballon", "C": "C comme Chocolat"}
}
NATURE_DATA = {
    "Animaux": {"Lion": "Le lion fait grrrr !", "Chat": "Le chat fait miaou.", "Chien": "Le chien fait ouaf !"},
    "Météo": {"Soleil": "Le soleil brille et il fait chaud !", "Pluie": "Il pleut, vite, un parapluie !", "Neige": "Il neige, on peut faire un bonhomme !"}
}
MONDE_DATA = {
    "Pays": {"France": "La capitale de la France est Paris.", "Espace": "La Lune tourne autour de la Terre."},
    "Transports": {"Voiture": "La voiture roule sur la route.", "Avion": "L'avion vole très haut dans les nuages."}
}

# --- 4. DESIGN ARC-EN-CIEL ET VISIBILITÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    .titre-enfant { 
        text-align: center; 
        font-family: 'Fredoka One'; 
        color: #5E35B1 !important; 
        font-size: 50px; 
        text-shadow: 3px 3px 0px #FFFFFF;
        margin-bottom: 30px;
    }

    /* BOUTONS AVEC TEXTE VIOLET FONCÉ ET BORDURE ARC-EN-CIEL */
    .stButton > button { 
        background: white !important; 
        color: #4A148C !important; 
        font-family: 'Fredoka One' !important; 
        font-size: 24px !important; 
        min-height: 95px !important; 
        width: 100% !important;
        border: 6px solid !important;
        border-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) 1 !important;
        box-shadow: 0px 6px 0px #D1C4E9 !important;
        margin-bottom: 15px !important;
    }

    /* Champs de texte */
    input, textarea { color: #4A148C !important; font-weight: bold !important; font-size: 20px !important; }
    p, span, label { color: #311B92 !important; font-family: 'Fredoka One', sans-serif !important; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    if txt:
        try:
            tts = gTTS(text=str(txt), lang='fr')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            b64 = base64.b64encode(fp.getvalue()).decode()
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        except: pass

# --- 5. LOGIQUE DE NAVIGATION ---

# --- PAGE D'ACCUEIL ---
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

# --- DOSSIERS D'APPRENTISSAGE ---
elif st.session_state.mode == "jeu":
    if st.button("🏠 RETOUR ACCUEIL"): st.session_state.mode = "accueil"; st.rerun()
    
    if not st.session_state.chemin:
        st.markdown("<h2 style='text-align:center;'>Choisis un dossier :</h2>", unsafe_allow_html=True)
        u1, u2 = st.columns(2)
        if u1.button("🏫 L'ÉCOLE"): st.session_state.chemin = ["ECOLE"]; st.rerun()
        if u1.button("🦁 LA NATURE"): st.session_state.chemin = ["NATURE"]; st.rerun()
        if u2.button("🌍 LE MONDE"): st.session_state.chemin = ["MONDE"]; st.rerun()
    else:
        if st.button("⬅️ DOSSIER PRÉCÉDENT"): st.session_state.chemin.pop(); st.rerun()
        
        MASTER_DATA = {"ECOLE": ECOLE_DATA, "NATURE": NATURE_DATA, "MONDE": MONDE_DATA}
        contenu = MASTER_DATA
        for d in st.session_state.chemin:
            contenu = contenu.get(d, {})
        
        cols = st.columns(2)
        for idx, (k, v) in enumerate(contenu.items()):
            with cols[idx % 2]:
                if st.button(f"{'📁' if isinstance(v, dict) else '🔊'} {k}"):
                    if isinstance(v, dict):
                        st.session_state.chemin.append(k)
                        st.rerun()
                    else:
                        parler(v)
                        st.info(v)

# --- COIN JEUX ---
elif st.session_state.mode == "menu_jeux":
    st.markdown("<h1 class='titre-enfant'>🎮 COIN JEUX</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    cj1, cj2 = st.columns(2)
    with cj1:
        if st.button("🦖 JEU DU DINOSAURE"): st.session_state.mode = "jouer_dino"; st.rerun()
    with cj2:
        if st.button("🔢 CHIFFRE CACHÉ"): st.session_state.mode = "cache"; st.rerun()

# --- LANCEUR DINO GITHUB ---
elif st.session_state.mode == "jouer_dino":
    if st.button("⬅️ RETOUR AUX JEUX"): st.session_state.mode = "menu_jeux"; st.rerun()
    st.markdown("<h2 style='text-align:center;'>🦖 COURSE DE DINO</h2>", unsafe_allow_html=True)
    url_jeu = "https://zachariepays-debug.github.io/jeux-magiques/dino.html"
    st.components.v1.iframe(url_jeu, height=600, scrolling=False)

# --- MACHINE À PHRASES ---
elif st.session_state.mode == "parleur":
    st.markdown("<h1 class='titre-enfant'>🗣️ MACHINE À PHRASES</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    phrase = st.text_area("Tape ta phrase ici (je vais la dire) :", height=150)
    if st.button("🔊 FAIRE PARLER"):
        if phrase: parler(phrase)

# --- CALCULS ---
elif st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>🧮 CALCULATRICE</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.session_state.calc_val = ""; st.rerun()
    st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; font-size:45px; color:#4A148C; text-align:center; border:4px solid #5E35B1;'>{st.session_state.calc_val if st.session_state.calc_val else '0'}</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    touches = ["1","2","3","4","5","6","7","8","9","+","0","-"]
    for idx, t in enumerate(touches):
        if [c1, c2, c3][idx % 3].button(t):
            st.session_state.calc_val += t
            st.rerun()
    if st.button("⭐ ÉGAL"):
        try:
            res = eval(st.session_state.calc_val)
            parler(f"Ça fait {res}")
            st.session_state.calc_val = str(res)
        except: st.session_state.calc_val = ""
        st.rerun()

# --- DICO & DOUDOU ---
elif st.session_state.mode in ["dict", "ia"]:
    nom = "📖 LE DICO" if st.session_state.mode == "dict" else "🤖 DOUDOU"
    st.markdown(f"<h1 class='titre-enfant'>{nom}</h1>", unsafe_allow_html=True)
    if st.button("🏠 RETOUR"): st.session_state.mode = "accueil"; st.rerun()
    question = st.text_input("Écris ici :")
    if st.button("DEMANDER"):
        if question:
            # Note: Remets ici ton code Mistral si tu as la clé API
            rep = "Je suis ton ami Doudou !"
            st.success(rep)
            parler(rep)
