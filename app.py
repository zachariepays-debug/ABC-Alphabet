import streamlit as st
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈✨", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LE DESIGN "EXACTEMENT COMME L'IMAGE" ---
design_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond Arc-en-ciel Pastel */
    .stApp {
        background: linear-gradient(135deg, #BFF0FA 0%, #E0C3FC 50%, #FFD6E8 100%);
        background-attachment: fixed;
    }

    /* Ajout des Confettis et Étoiles partout en fond */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(circle, #FFD700 20%, transparent 20%),
            radial-gradient(circle, #FF69B4 20%, transparent 20%),
            radial-gradient(circle, #00BFFF 20%, transparent 20%),
            radial-gradient(circle, #32CD32 20%, transparent 20%);
        background-size: 150px 150px, 200px 200px, 180px 180px, 250px 250px;
        background-position: 0 0, 50px 50px, 100px 100px, 30px 80px;
        opacity: 0.3;
        z-index: -1;
        pointer-events: none;
    }

    /* Titre Monde Magique */
    .titre-magique {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 75px !important;
        color: #8A63FF !important;
        text-shadow: 4px 4px 0px white, 0px 0px 20px rgba(138, 99, 255, 0.4);
        margin: 50px 0;
    }

    /* Boutons blancs avec bords violets et petites étoiles */
    .stButton > button {
        background-color: white !important;
        color: #5D3FD3 !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 24px !important;
        border: 5px solid #8A63FF !important;
        border-radius: 40px !important;
        height: 110px !important;
        width: 100% !important;
        box-shadow: 0px 10px 0px #6A39D9 !important;
        margin-bottom: 25px !important;
        transition: all 0.2s;
        /* Petites étoiles décoratives sur le bouton */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23FFD700' d='M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: 15px 15px;
        background-size: 25px;
    }

    .stButton > button:active {
        transform: translateY(6px);
        box-shadow: 0px 4px 0px #6A39D9 !important;
    }

    /* Écran de chargement avec les mêmes couleurs */
    .loading-screen {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: linear-gradient(135deg, #BFF0FA 0%, #E0C3FC 50%, #FFD6E8 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        z-index: 9999;
    }
</style>
"""

# --- 3. LOGIQUE DU CHARGEMENT ---
if 'fini' not in st.session_state:
    st.markdown(design_css, unsafe_allow_html=True)
    load = st.empty()
    with load.container():
        st.markdown("""
            <div class="loading-screen">
                <div style="font-size:150px; animation: bounce 1s infinite alternate;">✨</div>
                <h1 style="font-family:'Fredoka One'; color:#8A63FF; font-size:50px;">MAGIE EN COURS...</h1>
                <div style="width:300px; height:20px; background:white; border-radius:10px; border:4px solid #8A63FF; overflow:hidden;">
                    <div style="width:100%; height:100%; background:linear-gradient(90deg, #FF1493, #00BFFF, #00FF7F); animation: grow 3s linear infinite;"></div>
                </div>
            </div>
            <style>
                @keyframes bounce { from {transform:translateY(0);} to {transform:translateY(-50px);} }
                @keyframes grow { from {transform:translateX(-100%);} to {transform:translateX(100%);} }
            </style>
        """, unsafe_allow_html=True)
        time.sleep(4)
    st.session_state.fini = True
    load.empty()

# --- 4. LE SITE FINAL ---
st.markdown(design_css, unsafe_allow_html=True)

# Décorations de coins (comme sur l'image)
st.markdown("<div style='position:fixed; top:0; left:0; font-size:100px;'>🌈</div>", unsafe_allow_html=True)
st.markdown("<div style='position:fixed; top:0; right:0; font-size:100px;'>⭐</div>", unsafe_allow_html=True)

st.markdown("<h1 class='titre-magique'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# Grille de dossiers
c1, c2 = st.columns(2)

with c1:
    st.button("📚 ÉCOLE", key="b1")
    st.button("🧮 CALCULS", key="b2")
    st.button("🔊 COMPTER (0 à 100)", key="b3")
    st.button("📁 LES MATHS ➕", key="b4")

with c2:
    st.button("🤖 DOUDOU IA", key="b5")
    st.button("📖 DÉFINITION", key="b6")
    st.button("📁 L'ALPHABET ⭐", key="b7")
    st.button("🍎 LE MARCHÉ GÉANT", key="b8")
