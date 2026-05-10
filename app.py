import streamlit as st
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈✨", layout="wide", initial_sidebar_state="collapsed")

# Initialisation de la navigation dans l'état de la session
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# --- 2. LE STYLE "FÊTE TOTALE" (Chargement + Site) ---
style_total = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond Arc-en-ciel animé */
    .stApp, .loading-screen {
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* Décorations : Ballons et Étoiles */
    .stApp::before, .loading-screen::before {
        content: '🎈 ✨ 🌟 🎈 🎊 🌟 🎈 ✨ 🌟 🎈 🎊 🌟';
        position: fixed;
        top: -100px;
        left: 0;
        width: 100%;
        height: 300%;
        font-size: 45px;
        line-height: 180px;
        word-spacing: 150px;
        color: rgba(255, 255, 255, 0.45);
        z-index: -1;
        pointer-events: none;
        animation: float_magic 25s linear infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes float_magic {
        from { transform: translateY(0); }
        to { transform: translateY(-50%); }
    }

    /* Boutons ronds et colorés avec le style de l'image */
    .stButton > button {
        background: white !important;
        border: 4px solid #8A63FF !important;
        border-radius: 25px !important;
        color: #8A63FF !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 20px !important;
        height: 80px !important;
        box-shadow: 0px 6px 0px #8A63FF !important;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }

    .stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0px 2px 0px #8A63FF !important;
    }
    
    .stButton > button:hover {
        background: #F0E6FF !important;
    }

    /* Titre central */
    .titre-magique {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 70px !important;
        color: #8A63FF !important;
        text-shadow: 4px 4px 0px white;
        margin-top: 30px;
        margin-bottom: 40px;
    }
    
    /* Titre des pages internes */
    .titre-page {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 50px !important;
        color: #FF6B6B !important;
        text-shadow: 2px 2px 0px white;
    }
</style>
"""

# --- 3. CHARGEMENT INITIAL ---
if 'chargement_fini' not in st.session_state:
    st.markdown(style_total, unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="loading-screen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 9999;">
                <div style="font-size: 120px; animation: bounce 1s infinite alternate;">🎁</div>
                <h1 style="font-family: 'Fredoka One', cursive; color: #8A63FF; text-shadow: 3px 3px 0px white;">ON PRÉPARE LA MAGIE... ✨</h1>
            </div>
            <style>
                @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-40px); } }
            </style>
        """, unsafe_allow_html=True)
        time.sleep(2) # Réduit à 2 secondes pour être plus rapide
    st.session_state.chargement_fini = True
    placeholder.empty()

# Appliquer le style global
st.markdown(style_total, unsafe_allow_html=True)

# --- 4. LOGIQUE DE NAVIGATION (LE SITE) ---

# FONCTION POUR CHANGER DE PAGE
def changer_page(nouvelle_page):
    st.session_state.page = nouvelle_page

# AFFICHAGE DU MENU PRINCIPAL
if st.session_state.page == 'menu':
    
    # Ligne du haut (4 boutons)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📚 ÉCOLE", use_container_width=True): changer_page('ecole')
    with col2:
        if st.button("🧮 CALCULS", use_container_width=True): changer_page('calculs')
    with col3:
        if st.button("📖 DÉFINITION", use_container_width=True): changer_page('definition')
    with col4:
        if st.button("🤖 DOUDOU IA", use_container_width=True): changer_page('doudou_ia')

    # Titre au centre
    st.markdown("<h1 class='titre-magique'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

    # Lignes du bas (2 colonnes comme sur l'image)
    c_gauche, c_droite = st.columns(2)

    with c_gauche:
        if st.button("🔊 🔢 COMPTER (0 à 100)", use_container_width=True): changer_page('compter')
        if st.button("📁 ➕ LES MATHS", use_container_width=True): changer_page('maths')
        if st.button("📁 📅 LE CALENDRIER", use_container_width=True): changer_page('calendrier')

    with c_droite:
        if st.button("📁 🔤 L'ALPHABET (A-Z)", use_container_width=True): changer_page('alphabet')
        if st.button("📁 🍎 LE MARCHÉ GÉANT", use_container_width=True): changer_page('marche')
        
        # Ajout d'un espace vide pour équilibrer la colonne de droite (optionnel)
        st.write("")

# --- 5. CONTENU DES DIFFÉRENTES PAGES ---
else:
    # Bouton de retour commun à toutes les pages
    if st.button("⬅️ Retour au Monde Magique", use_container_width=False):
        changer_page('menu')
        st.rerun()

    # Affichage selon la page sélectionnée
    if st.session_state.page == 'ecole':
        st.markdown("<h2 class='titre-page'>Bienvenue à l'École ! 📚</h2>", unsafe_allow_html=True)
        st.info("Mets ici le contenu de ton application École.")

    elif st.session_state.page == 'calculs':
        st.markdown("<h2 class='titre-page'>Place aux Calculs ! 🧮</h2>", unsafe_allow_html=True)
        st.info("Mets ici le contenu de ton application Calculs.")

    elif st.session_state.page == 'definition':
        st.markdown("<h2 class='titre-page'>Le coin des Définitions 📖</h2>", unsafe_allow_html=True)
        st.info("Mets ici le dictionnaire ou l'outil de définition.")

    elif st.session_state.page == 'doudou_ia':
        st.markdown("<h2 class='titre-page'>Bonjour, je suis Doudou IA ! 🤖</h2>", unsafe_allow_html=True)
        st.info("Intègre ici le chatbot ou l'assistant virtuel.")

    elif st.session_state.page == 'compter':
        st.markdown("<h2 class='titre-page'>Apprenons à compter jusqu'à 100 🔢</h2>", unsafe_allow_html=True)
        st.info("Mets ici ton module pour apprendre à compter.")

    elif st.session_state.page == 'alphabet':
        st.markdown("<h2 class='titre-page'>L'Alphabet de A à Z 🔤</h2>", unsafe_allow_html=True)
        st.info("Mets ici ton module pour l'alphabet.")

    elif st.session_state.page == 'maths':
        st.markdown("<h2 class='titre-page'>Les Mathématiques Faciles ➕</h2>", unsafe_allow_html=True)
        st.info("Mets ici les exercices de maths.")

    elif st.session_state.page == 'marche':
        st.markdown("<h2 class='titre-page'>Le Marché Géant 🍎</h2>", unsafe_allow_html=True)
        st.info("Mets ici le jeu du marché géant.")

    elif st.session_state.page == 'calendrier':
        st.markdown("<h2 class='titre-page'>Le Calendrier Magique 📅</h2>", unsafe_allow_html=True)
        st.info("Mets ici l'outil calendrier.")
