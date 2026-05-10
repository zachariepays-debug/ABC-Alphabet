import streamlit as st
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈✨", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LE STYLE "FÊTE TOTALE" (Chargement + Site) ---
# Ce bloc CSS injecte les confettis et les ballons sur toutes les pages
style_total = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond Arc-en-ciel animé qui ne s'arrête jamais */
    .stApp, .loading-screen {
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* Décorations : Ballons et Étoiles qui flottent en arrière-plan */
    /* On les met sur .stApp pour qu'ils soient partout sur le site */
    .stApp::before, .loading-screen::before {
        content: '🎈 ✨ 🌟 🎈 ✨ 🌟 🎈 ✨ 🌟 🎈 ✨ 🌟';
        position: fixed;
        top: -100px;
        left: 0;
        width: 100%;
        height: 300%;
        font-size: 45px;
        line-height: 180px;
        word-spacing: 200px;
        color: rgba(255, 255, 255, 0.45); /* Un peu transparent pour lire facilement */
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

    /* Boutons ronds et colorés */
    .stButton > button {
        background: white !important;
        border: 5px solid #8A63FF !important;
        border-radius: 35px !important;
        color: #8A63FF !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 22px !important;
        height: 90px !important;
        box-shadow: 0px 8px 0px #8A63FF !important;
        margin-bottom: 15px;
    }

    .stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0px 2px 0px #8A63FF !important;
    }

    .titre-magique {
        text-align: center;
        font-family: 'Fredoka One', cursive !important;
        font-size: 60px !important;
        color: #8A63FF !important;
        text-shadow: 3px 3px 0px white;
    }
</style>
"""

# --- 3. CHARGEMENT (Avec le même décor) ---
if 'chargement_fini' not in st.session_state:
    st.markdown(style_total, unsafe_allow_html=True)
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="loading-screen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 9999;">
                <div style="font-size: 120px; animation: bounce 1s infinite alternate;">🎁</div>
                <h1 style="font-family: 'Fredoka One', cursive; color: #8A63FF; text-shadow: 3px 3px 0px white;">ON PRÉPARE LES JEUX... ✨</h1>
            </div>
            <style>
                @keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-40px); } }
            </style>
        """, unsafe_allow_html=True)
        time.sleep(3)
    st.session_state.chargement_fini = True
    placeholder.empty()

# --- 4. LE SITE (Toujours avec le décor) ---
st.markdown(style_total, unsafe_allow_html=True)

st.markdown("<h1 class='titre-magique'>MONDE MAGIQUE ✨</h1>", unsafe_allow_html=True)

# Disposition des boutons
c1, c2 = st.columns(2)

with c1:
    st.button("📚 ÉCOLE", use_container_width=True)
    st.button("🧮 CALCULS", use_container_width=True)
    st.button("🔊 COMPTER", use_container_width=True)

with c2:
    st.button("🤖 DOUDOU IA", use_container_width=True)
    st.button("📖 DÉFINITION", use_container_width=True)
    st.button("🍎 LE MARCHÉ", use_container_width=True)
