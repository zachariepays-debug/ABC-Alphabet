import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IMPORT DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    st.error("Oups ! Les doudous sont perdus !")

# --- 3. DESIGN "MAGIQUE & POP" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* Fond dégradé pastel animé */
    .stApp {{ 
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}

    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .titre-enfant {{ 
        text-align: center; 
        color: #FF69B4; 
        font-size: 42px; 
        font-family: 'Fredoka One', cursive;
        text-shadow: 3px 3px 0px #FFF;
        margin-bottom: 10px;
    }}

    .slogan {{
        text-align: center;
        color: #7B68EE;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 25px;
    }}

    /* Boutons Dossiers (Jaune Doux) */
    .btn-dossier button {{
        background: #FFF2B2 !important; 
        border: 5px solid #FFCC00 !important;
        height: 120px !important; 
        font-size: 28px !important; 
        border-radius: 40px !important;
        color: #FF5500 !important; 
        margin-bottom: 15px !important;
        box-shadow: 0px 10px 0px #FFB300 !important;
        font-family: 'Fredoka One', cursive !important;
    }}
    
    /* Objets Arc-en-ciel Pastel */
    .btn-objet:nth-child(5n+1) button {{ background: #FFD6E8 !important; border: 4px solid #FF85B3 !important; box-shadow: 0px 8px 0px #FF5C9D !important; }}
    .btn-objet:nth-child(5n+2) button {{ background: #C9F2FF !important; border: 4px solid #70D1F4 !important; box-shadow: 0px 8px 0px #3EADE2 !important; }}
    .btn-objet:nth-child(5n+3) button {{ background: #D8FFF1 !important; border: 4px solid #85E3B3 !important; box-shadow: 0px 8px 0px #5BCB8E !important; }}
    .btn-objet:nth-child(5n+4) button {{ background: #E5D9FF !important; border: 4px solid #B194FF !important; box-shadow: 0px 8px 0px #8A63FF !important; }}
    .btn-objet:nth-child(5n+5) button {{ background: #FFF2B2 !important; border: 4px solid #F4D03F !important; box-shadow: 0px 8px 0px #D4AC0D !important; }}

    .btn-objet button {{
        height: 100px !important; 
        font-size: 26px !important; 
        border-radius: 35px !important;
        color: #444 !important; 
        margin-bottom: 15px !important;
        font-family: 'Fredoka One', cursive !important;
    }}

    .btn-retour button {{
        background: #FF69B4 !important; 
        color: white !important;
        height: 70px !important; 
        border-radius: 50px !important;
        font-size: 20px !important;
        border: 4px solid white !important;
        box-shadow: 0px 5px 15px rgba(255, 105, 180, 0.4) !important;
    }}
    
    .nav-bar {{ 
        background: rgba(255,255,255,0.7); 
        padding: 15px; 
        border-radius: 60px; 
        display: flex; 
        justify-content: center; 
        gap: 15px; 
        box-shadow: 0px 10px 30px rgba(0,0,0,0.05); 
        margin-bottom: 30px; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE AUDIO ---
def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. ÉTATS ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Navigation
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        if st.button(icons[i], key=f"nav_{i}"):
            st.session_state.slide = i+1
            st.session_state.chemin = []
            st.rerun()

# Données
mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
contenu = mapping[st.session_state.slide]
for dossier in st.session_state.chemin:
    contenu = contenu[dossier]

# Affichage
if len(st.session_state.chemin) > 0:
    st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
    if st.button("💝 ON REVIENT !", key="back"):
        st.session_state.chemin.pop()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<h1 class='titre-enfant'>{'✨ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'MONDE MAGIQUE 🎈'}</h1>", unsafe_allow_html=True)
st.markdown("<p class='slogan'>Jouer, découvrir, grandir 💖</p>", unsafe_allow_html=True)

# Boutons
if isinstance(contenu, dict):
    for nom, valeur in contenu.items():
        if isinstance(valeur, (dict, list)) and not isinstance(valeur, str):
            st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
            if st.button(f"🐾 {nom}", key=f"d_{nom}"):
                st.session_state.chemin.append(nom)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
            if st.button(nom, key=f"i_{nom}"):
                parler(valeur)
            st.markdown('</div>', unsafe_allow_html=True)
elif isinstance(contenu, list):
    for item in contenu:
        st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
        if st.button(str(item), key=f"l_{item}"):
            parler(item)
        st.markdown('</div>', unsafe_allow_html=True)
