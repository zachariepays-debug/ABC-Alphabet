import streamlit as st
import base64
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="MONDE MAGIQUE 🎈✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. ÉCRAN DE CHARGEMENT ARC-EN-CIEL (5 SECONDES) ---
if "chargement_fini" not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
            
            /* Fond animé commun */
            .magic-bg-loading {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
                background-size: 400% 400%; animation: gradient_bg 15s ease infinite;
                z-index: -2;
            }
            
            /* Décorations flottantes (étoiles, ballons) sur le chargement */
            .magic-bg-loading::after {
                content: '🎈 ✨ ⭐ 🎁 🎉';
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                font-size: 35px; line-height: 120px; word-spacing: 180px;
                color: rgba(255,255,255,0.4); pointer-events: none; z-index: -1;
                animation: float_bg 10s infinite linear;
            }

            @keyframes gradient_bg {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            @keyframes float_bg {
                from { transform: translateY(0); }
                to { transform: translateY(-100px); }
            }

            /* Contenu spécifique au chargement */
            .loading-content {
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                height: 100vh; font-family: 'Fredoka One', cursive; z-index: 9999;
            }
            .ballon-load { font-size: 130px; animation: bounce_ballon 1s infinite alternate; }
            @keyframes bounce_ballon { from { transform: translateY(0); } to { transform: translateY(-40px); } }
            .txt-load { color: #2C3E50; font-size: 40px; margin-top: 30px; text-shadow: 2px 2px 0px white; }
            .rainbow-bar { width: 350px; height: 25px; background: white; border-radius: 12px; margin-top: 30px; overflow: hidden; border: 4px solid #FFF; }
            .rainbow-progress { width: 100%; height: 100%; background: linear-gradient(to right, #FF1493, #00BFFF, #00FF7F, #FFD700); animation: slide_rainbow 2s linear infinite; }
            @keyframes slide_rainbow { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
            </style>
            
            <div class="magic-bg-loading"></div>
            <div class="loading-content">
                <div class="ballon-load">🎈</div>
                <div class="txt-load">Création de la magie... ✨</div>
                <div class="rainbow-bar"><div class="rainbow-progress"></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(5)
    st.session_state.chargement_fini = True
    placeholder.empty()

# --- 3. DESIGN GLOBAL DÉCORÉ (APRÈS CHARGEMENT) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* === A. FOND ARC-EN-CIEL ET DÉCORS FLOTTANTS === */
    .stApp {
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient_bg_app 15s ease infinite;
        position: relative;
    }

    @keyframes gradient_bg_app {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Décorations (étoiles, ballons, confettis) flottantes */
    .stApp::before {
        content: '✨ ⭐ 🎈 ✨ 🎁 ⭐ 🎉 ✨ 🎈 ⭐ ✨';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        font-size: 35px; line-height: 120px; word-spacing: 180px;
        color: rgba(255, 255, 255, 0.4);
        pointer-events: none; z-index: -1;
        animation: float_decorations 10s infinite linear;
    }

    @keyframes float_decorations {
        from { transform: translateY(0); }
        to { transform: translateY(-100px); }
    }

    /* === B. TITRE ET TEXTES === */
    .titre-magique {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 65px !important;
        color: #8A63FF !important;
        text-shadow: 4px 4px 0px #FFFFFF, 6px 6px 0px rgba(0,0,0,0.1);
        margin: 40px 0;
    }

    /* === C. BOUTONS STYLISÉS "TOY-STYLE" === */
    /* On modifie TOUS les boutons Streamlit */
    .stButton > button {
        background: #FFFFFF !important;
        color: #8A63FF !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: 5px solid #8A63FF !important;
        height: 100px !important;
        width: 100% !important;
        box-shadow: 0px 8px 0px #6A39D9 !important;
        margin-bottom: 20px !important;
        position: relative;
        overflow: visible; /* Pour les emojis qui dépassent */
    }

    /* Effet d'enfoncement au clic */
    .stButton > button:active {
        box-shadow: 0px 3px 0px #6A39D9 !important;
        transform: translateY(4px);
    }

    /* === D. DÉCORATIONS INDIVIDUELLES DES BOUTONS === */
    /* On utilise l'emoji dans le texte pour décorer, pas de CSS complexe ici pour la stabilité */

    </style>
    """,
    unsafe_allow_html=True,
)

# --- 4. AFFICHAGE DES ÉLÉMENTS DU SITE ---

# A. Le grand titre décoré
st.markdown("<h1 class='titre-magique'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# B. La grille des boutons (en 2 colonnes comme sur l'image)
# On utilise des colonnes Streamlit pour reproduire la grille
c1, c2 = st.columns(2)

with c1:
    st.button("📚 ÉCOLE", key="ecole")
    st.button("🧮 CALCULS", key="calculs")
    st.button("📖 DÉFINITION", key="definition")
    st.button("🔊 COMPTER (0 à 100)", key="compter")
    # Button avec petite étoile déco intégrée
    st.button("📁 LES MATHS ⭐", key="maths")

with c2:
    # Button avec ballon déco intégré
    st.button("🎈 DOUDOU IA", key="doudou")
    # Buttons avec petite étoile déco intégrée
    st.button("📁 L'ALPHABET (A-Z) ⭐", key="alphabet")
    st.button("📁 LE MARCHÉ GÉANT ⭐", key="marche")
    st.button("📁 LE CALENDRIER ⭐", key="calendrier")

# --- 5. LOGIQUE DE JEU (Exemple) ---
# (C'est ici que tu mettrais ton code pour lancer les sons, l'IA, etc.)
if st.session_state.get("ecole"):
    st.balloon() # Petite animation pour le fun
    # tts_parler("Bienvenue à l'école magique !")
