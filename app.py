import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ET DESIGN BÉBÉ ---
st.set_page_config(page_title="App Bébé", page_icon="🧸", layout="centered")

st.markdown("""
    <style>
    /* Fond de l'application doux (Bleu pastel très clair) */
    .stApp {
        background-color: #F4F9FF;
    }
    /* Style général des boutons (Gros, arrondis, ombres) */
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 30px !important;
        font-weight: bold;
        border-radius: 20px;
        border: 4px solid #FFD1DC; /* Rose pastel */
        background-color: #FFFFFF;
        color: #4A4A4A;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
        transition: 0.2s;
    }
    /* Changement de couleur au survol */
    div.stButton > button:hover {
        border-color: #87CEFA; /* Bleu ciel */
        transform: scale(1.02);
    }
    /* Titres colorés */
    h1 { color: #FF69B4; text-align: center; font-size: 50px !important; }
    h2, h3 { color: #20B2AA; text-align: center; }
    /* Case d'affichage pour les mots */
    .ecran-texte {
        text-align: center; 
        font-size: 40px; 
        font-weight: bold; 
        color: #333;
        border: 4px dashed #FFB6C1; 
        padding: 20px; 
        border-radius: 20px; 
        background: white;
        min-height: 90px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'phrase' not in st.session_state:
    st.session_state.phrase = ""
if 'suite_chiffres' not in st.session_state:
    st.session_state.suite_chiffres = ""

def changer_page(nouvelle_page):
    st.session_state.page = nouvelle_page
    st.session_state.phrase = ""
    st.session_state.suite_chiffres = ""
    st.rerun()

# --- 3. FONCTION POUR LA VOIX ---
def parler(texte):
    if not texte: return
    try:
        tts = gTTS(text=str(texte), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_b64 = base64.b64encode(fp.getvalue()).decode()
        html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
        st.markdown(html_string, unsafe_allow_html=True)
    except:
        pass

# ==========================================
#              LES DIFFÉRENTES PAGES
# ==========================================

# 🏠 PAGE : MENU PRINCIPAL
if st.session_state.page == "menu":
    st.title("🧸 Jeux pour Bébé")
    st.write("### Choisis une activité !")
    
    st.write("")
    if st.button("🔤 Apprendre l'Alphabet"): changer_page("alphabet")
    if st.button("🔢 Apprendre les Chiffres"): changer_page("chiffres")
    if st.button("✍️ Écrire des Mots"): changer_page("mots")
    if st.button("📱 Écrire des Numéros"): changer_page("numeros")
    
    # Coin admin tout en bas, très discret
    st.write("---")
    c1, c2 = st.columns([0.8, 0.2])
    with c2:
        if st.button("Admin"): st.session_state.show_admin = not st.session_state.get('show_admin', False)
    if st.session_state.get('show_admin', False):
        pwd = st.text_input("Code secret", type="password")
        if pwd == "babar":
            st.success("Accès Admin : Tout fonctionne parfaitement.")

# 🔤 PAGE : ALPHABET SIMPLE
elif st.session_state.page == "alphabet":
    if st.button("🏠 Retour au Menu"): changer_page("menu")
    st.title("🔤 L'Alphabet")
    
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i in range(0, len(alphabet), 5): # 5 lettres par ligne
        cols = st.columns(5)
        for j, lettre in enumerate(alphabet[i:i+5]):
            with cols[j]:
                if st.button(lettre, key=f"A_{lettre}"):
                    parler(lettre)

# 🔢 PAGE : CHIFFRES SIMPLES
elif st.session_state.page == "chiffres":
    if st.button("🏠 Retour au Menu"): changer_page("menu")
    st.title("🔢 Les Chiffres")
    
    chiffres = list("0123456789")
    for i in range(0, len(chiffres), 5): # 5 chiffres par ligne
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"C_{chiffre}"):
                    parler(chiffre)

# ✍️ PAGE : MACHINE À MOTS
elif st.session_state.page == "mots":
    if st.button("🏠 Retour au Menu"): changer_page("menu")
    st.title("✍️ Machine à Mots")
    
    # Écran d'affichage du mot
    affichage = st.session_state.phrase if st.session_state.phrase else "..."
    st.markdown(f"<div class='ecran-texte'>{affichage}</div>", unsafe_allow_html=True)
    
    # Boutons de contrôle
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔊 Lire"): parler(st.session_state.phrase)
    with col2:
        if st.button("Espace"): 
            st.session_state.phrase += " "
            st.rerun()
    with col3:
        if st.button("🗑️ Effacer"): 
            st.session_state.phrase = ""
            st.rerun()

    st.write("---")
    
    # Clavier pour écrire
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"M_{lettre}"):
                    st.session_state.phrase += lettre
                    parler(lettre)
                    st.rerun()

# 📱 PAGE : MACHINE À NUMÉROS
elif st.session_state.page == "numeros":
    if st.button("🏠 Retour au Menu"): changer_page("menu")
    st.title("📱 Machine à Numéros")
    
    # Écran d'affichage des chiffres
    affichage = st.session_state.suite_chiffres if st.session_state.suite_chiffres else "..."
    st.markdown(f"<div class='ecran-texte' style='border-color: #87CEFA;'>{affichage}</div>", unsafe_allow_html=True)
    
    # Boutons de contrôle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 Lire tout"): parler(st.session_state.suite_chiffres)
    with col2:
        if st.button("🗑️ Effacer"): 
            st.session_state.suite_chiffres = ""
            st.rerun()

    st.write("---")
    
    # Clavier des chiffres
    chiffres = list("0123456789")
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"N_{chiffre}"):
                    st.session_state.suite_chiffres += chiffre
                    parler(chiffre)
                    st.rerun()
