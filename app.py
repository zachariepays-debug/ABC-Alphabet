import streamlit as st
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈✨", layout="wide", initial_sidebar_state="collapsed")

# --- 2. STYLE CSS (POUR LE CHARGEMENT ET LE SITE) ---
# Ce code crée le fond arc-en-ciel + les confettis et ballons qui flottent
style_magique = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond animé arc-en-ciel doux */
    .stApp, .loading-screen {
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Décorations Confettis, Ballons et Étoiles (partout en fond) */
    .stApp::before, .loading-screen::before {
        content: '🎈 ✨ 🌟 🎈 ✨ 🌟 🎈 ✨ 🌟';
        position: fixed;
        top: -50px;
        left: 0;
        width: 100%;
        height: 200%;
        font-size: 40px;
        line-height: 150px;
        word-spacing: 250px;
        color: rgba(255, 255, 255, 0.4);
        z-index: -1;
        pointer-events: none;
        animation: float 20s linear infinite;
    }

    @keyframes float {
        from { transform: translateY(0); }
        to { transform: translateY(-50%); }
    }

    /* Style des boutons (gros et ronds comme sur l'image) */
    .stButton > button {
        background: white !important;
        border: 4px solid #8A63FF !important;
        border-radius: 30px !important;
        color: #8A63FF !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 20px !important;
        height: 80px !important;
        box-shadow: 0px 8px 0px #8A63FF !important;
        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 0px #8A63FF !important;
    }

    /* Titre magique */
    .titre-enfant {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 70px !important;
        color: #8A63FF !important;
        text-shadow: 4px 4px 0px white;
        margin-bottom: 50px;
    }
</style>
"""

# --- 3. PAGE DE CHARGEMENT ---
if 'chargement_fini' not in st.session_state:
    st.markdown(style_magique, unsafe_allow_html=True)
    placeholder = st.empty()
    
    with placeholder.container():
        # HTML de l'écran de chargement
        st.markdown("""
            <div class="loading-screen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 9999;">
                <div style="font-size: 150px; animation: bounce 1s infinite alternate;">🎈</div>
                <h1 style="font-family: 'Fredoka One', cursive; color: #8A63FF; text-shadow: 3px 3px 0px white;">LA MAGIE ARRIVE...</h1>
                <div style="width: 300px; height: 20px; background: white; border-radius: 10px; overflow: hidden; border: 3px solid #8A63FF;">
                    <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #FF1493, #00BFFF, #00FF7F, #FFD700); animation: progress 3s linear infinite;"></div>
                </div>
                <style>
                    @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-50px); } }
                    @keyframes progress { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
                </style>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(4) # Durée du chargement
    
    st.session_state.chargement_fini = True
    placeholder.empty()

# --- 4. LE SITE (CONTENU) ---
st.markdown(style_magique, unsafe_allow_html=True)

st.markdown("<h1 class='titre-enfant'>MONDE MAGIQUE</h1>", unsafe_allow_html=True)

# Grille de boutons comme sur ton image
col1, col2 = st.columns(2)

with col1:
    st.button("📚 ÉCOLE", use_container_width=True)
    st.button("🧮 CALCULS", use_container_width=True)
    st.button("🔊 COMPTER (0 à 100)", use_container_width=True)
    st.button("📁 LES MATHS", use_container_width=True)
    st.button("📁 LE CALENDRIER", use_container_width=True)

with col2:
    st.button("📖 DÉFINITION", use_container_width=True)
    st.button("🤖 DOUDOU IA", use_container_width=True)
    st.button("📁 L'ALPHABET (A-Z)", use_container_width=True)
    st.button("🍎 LE MARCHÉ GÉANT", use_container_width=True)
