import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION MOBILE & STYLE ---
st.set_page_config(page_title="Bébé Éveil Pro", page_icon="🌈", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(to bottom, #fdfbfb 0%, #ebedee 100%); }
    
    /* Boutons de menu principaux */
    .menu-btn > div > button {
        height: 120px !important;
        font-size: 28px !important;
        border-radius: 30px !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1) !important;
        border: none !important;
    }
    
    /* Boutons de jeux (lettres/chiffres) */
    div.stButton > button {
        width: 100%;
        height: 85px;
        font-size: 32px !important;
        font-weight: bold;
        border-radius: 20px;
        transition: 0.1s;
        border: 2px solid #fff;
    }
    
    .ecran-texte {
        text-align: center; font-size: 50px; font-weight: bold; 
        background: white; border-radius: 30px; padding: 20px;
        margin-bottom: 20px; border: 5px solid #FFD1DC;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE DE NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "menu"
if 'phrase' not in st.session_state: st.session_state.phrase = ""

def nav(p):
    st.session_state.page = p
    st.session_state.phrase = ""
    st.rerun()

def parler(txt):
    if not txt: return
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# ==========================================
#                PAGES DE JEUX
# ==========================================

# 🏠 MENU PRINCIPAL
if st.session_state.page == "menu":
    st.markdown("<h1 style='text-align:center; color:#FF6B6B;'>🌈 Bébé Éveil Pro</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="menu-btn">', unsafe_allow_html=True)
        if st.button("🔤 Lettres"): nav("alphabet")
        if st.button("🦁 Animaux"): nav("animaux")
        if st.button("🍎 Fruits"): nav("fruits")
        if st.button("🎹 Piano"): nav("piano")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="menu-btn">', unsafe_allow_html=True)
        if st.button("🔢 Chiffres"): nav("chiffres")
        if st.button("🎨 Couleurs"): nav("couleurs")
        if st.button("🚀 Véhicules"): nav("auto")
        if st.button("✍️ Écrire"): nav("mots")
        st.markdown('</div>', unsafe_allow_html=True)

# 🔤 ALPHABET
elif st.session_state.page == "alphabet":
    if st.button("⬅️ Menu"): nav("menu")
    alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cols = st.columns(4)
    for i, l in enumerate(alpha):
        with cols[i % 4]:
            if st.button(l, key=l): parler(l)

# 🔢 CHIFFRES
elif st.session_state.page == "chiffres":
    if st.button("⬅️ Menu"): nav("menu")
    nums = list("0123456789")
    cols = st.columns(3)
    for i, n in enumerate(nums):
        with cols[i % 3]:
            if st.button(n, key=n): parler(n)

# 🦁 ANIMAUX
elif st.session_state.page == "animaux":
    if st.button("⬅️ Menu"): nav("menu")
    anis = {"🐶":"Chien","🐱":"Chat","🐷":"Cochon","🦁":"Lion","🐘":"Éléphant","🐔":"Poule","🐸":"Grenouille","🦆":"Canard"}
    cols = st.columns(2)
    for i, (e, n) in enumerate(anis.items()):
        with cols[i % 2]:
            if st.button(f"{e}\n{n}"): parler(n)

# 🍎 FRUITS & LÉGUMES
elif st.session_state.page == "fruits":
    if st.button("⬅️ Menu"): nav("menu")
    frut = {"🍎":"Pomme","🍌":"Banane","🍓":"Fraise","🥕":"Carotte","🍅":"Tomate","🥦":"Brocoli"}
    cols = st.columns(2)
    for i, (e, n) in enumerate(frut.items()):
        with cols[i % 2]:
            if st.button(f"{e}\n{n}"): parler(n)

# 🚀 VÉHICULES
elif st.session_state.page == "auto":
    if st.button("⬅️ Menu"): nav("menu")
    vehi = {"🚗":"Voiture","🚒":"Pompiers","🚑":"Ambulance","✈️":"Avion","🚜":"Tracteur","🚁":"Hélicoptère"}
    cols = st.columns(2)
    for i, (e, n) in enumerate(vehi.items()):
        with cols[i % 2]:
            if st.button(f"{e}\n{n}"): parler(n)

# 🎨 COULEURS
elif st.session_state.page == "couleurs":
    if st.button("⬅️ Menu"): nav("menu")
    clrs = {"🔴":"Rouge","🔵":"Bleu","🟢":"Vert","🟡":"Jaune","🟠":"Orange","🟣":"Violet"}
    cols = st.columns(2)
    for i, (e, n) in enumerate(clrs.items()):
        with cols[i % 2]:
            if st.button(f"{e}\n{n}"): parler(n)

# 🎹 PIANO
elif st.session_state.page == "piano":
    if st.button("⬅️ Menu"): nav("menu")
    notes = {"DO":"Do","RÉ":"Ré","MI":"Mi","FA":"Fa","SOL":"Sol","LA":"La","SI":"Si"}
    for e, n in notes.items():
        if st.button(f"🎵 {e}", key=e): parler(n)

# ✍️ MACHINE À MOTS
elif st.session_state.page == "mots":
    if st.button("⬅️ Menu"): nav("menu")
    st.markdown(f"<div class='ecran-texte'>{st.session_state.phrase if st.session_state.phrase else '...'}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🔊"): parler(st.session_state.phrase)
    with c2:
        if st.button("␣"): st.session_state.phrase += " "; st.rerun()
    with c3:
        if st.button("🗑️"): st.session_state.phrase = ""; st.rerun()
    
    alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cols = st.columns(5)
    for i, l in enumerate(alpha):
        with cols[i % 5]:
            if st.button(l, key=f"kb_{l}"): 
                st.session_state.phrase += l
                parler(l)
                st.rerun()
