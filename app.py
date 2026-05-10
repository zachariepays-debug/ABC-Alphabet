import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# Récupération de la clé Mistral
try:
    MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
except:
    MISTRAL_API_KEY = None

# --- 2. IMPORT DES UNIVERS ---
try:
    from univers.ecole import ECOLE_DATA
    from univers.nature import NATURE_DATA
    from univers.monde import MONDE_DATA
    from univers.jeux import JEUX_DATA
except:
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 3. LOGIQUE IA (DOUDOU & DÉFINITIONS) ---
def ia_magique(prompt, mode="doudou"):
    if not MISTRAL_API_KEY:
        return "Branche ma clé magique !"
    
    system_instruction = """Tu es un doudou gentil pour enfant de 3 ans. 
    Si mode=dico: Donne UNIQUEMENT la définition du mot de façon très simple (ex: 'Un chat est un animal qui fait miaou'). Pas de phrases complexes.
    Si mode=doudou: Sois poli et joyeux. Phrases très courtes."""
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Mode={mode}. Réponds à : {prompt}"}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Le doudou se repose..."

# --- 4. DESIGN (LOOK BÉBÉ & CIEL MAGIQUE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    /* FOND MAGIQUE : CIEL DOUX DÉGRADÉ */
    .stApp {{ 
        background: linear-gradient(180deg, #A2D2FF 0%, #FEE1FF 100%);
        background-attachment: fixed;
    }}

    /* TEXTE STYLE ENFANT (ROND ET LISIBLE) */
    .titre-enfant, label, p, .stMarkdown, .stTextInput label {{ 
        color: #4A4A4A !important; 
        font-family: 'Fredoka One', cursive !important; 
    }}

    .titre-enfant {{ 
        text-align: center; 
        font-size: 50px !important; 
        color: #FF69B4 !important; 
        text-shadow: 3px 3px 0px white; 
        padding: 20px;
    }}

    /* BOUTONS "BULLES" ÉNORMES ET RONDS */
    .stButton > button {{ 
        background-color: #FFFFFF !important; 
        border: 6px solid #FFB6C1 !important; 
        border-radius: 50px !important; 
        color: #5D5D5D !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 24px !important; 
        transition: transform 0.3s ease;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.1) !important;
        margin-bottom: 10px;
        height: auto !important;
        padding: 15px 30px !important;
    }}

    .stButton > button:hover {{
        transform: scale(1.05);
        border-color: #87CEEB !important;
    }}

    /* CHAMPS DE TEXTE COMME DES PETITS NUAGES BLANCS */
    input {{ 
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.9) !important; 
        border: 4px solid #BDE0FE !important;
        border-radius: 30px !important;
        padding: 15px !important;
        font-size: 22px !important;
        text-align: center;
    }}

    /* COULEURS DES BOUTONS DE JEU */
    .btn-dossier button {{ 
        background: #FFD700 !important; 
        border: 6px solid #FFA500 !important; 
        color: white !important; 
    }}
    
    .btn-objet button {{ 
        background: #98FB98 !important; 
        border: 6px solid #3CB371 !important; 
        color: #2E8B57 !important; 
    }}

    .btn-retour button {{ 
        background: #FF6347 !important; 
        color: white !important; 
        border: 6px solid #FFFFFF !important; 
    }}

    /* NETTOYAGE DE L'INTERFACE (PLUS PROPRE POUR LES PETITS) */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. NAVIGATION ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📚 ÉCOLE"): st.session_state.mode, st.session_state.slide, st.session_state.chemin = "jeu", 1, []
with c2: 
    if st.button("🧮 CALCULS"): st.session_state.mode = "calc"
with c3: 
    if st.button("📖 MOTS"): st.session_state.mode = "dict"
with c4: 
    if st.button("🤖 DOUDOU"): st.session_state.mode = "ia"

st.write("---")

# --- MODES ---
if st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>Ma Calculatrice 🧮</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER LE NOMBRE"): parler(n)

elif st.session_state.mode == "dict":
    st.markdown("<h1 class='titre-enfant'>Définition 📖</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    mot_saisi = st.text_input("Écris un mot :", placeholder="Ex: Chat")
    
    if st.button("🌟 C'EST QUOI ?"):
        if mot_saisi:
            definition = ia_magique(mot_saisi, mode="dico")
            st.success(definition)
            parler(definition)

elif st.session_state.mode == "ia":
    st.markdown("<h1 class='titre-enfant'>Doudou IA 🤖</h1>", unsafe_allow_html=True)
    if st.button("⬅️ RETOUR"): st.session_state.mode = "jeu"
    q = st.text_input("Parle à ton doudou :", placeholder="Coucou !")
    if st.button("RÉPONDRE"):
        rep = ia_magique(q, mode="doudou")
        st.info(rep)
        parler(rep)

else:
    # Système de jeu univers
    cols = st.columns(3)
    btns = ["🦁 NATURE", "🌍 MONDE", "🎁 JEUX"]
    for i, t in enumerate(btns):
        if cols[i].button(t): 
            st.session_state.slide = i + 2
            st.session_state.chemin = []
            st.rerun()

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping.get(st.session_state.slide, {})
    for d in st.session_state.chemin: 
        if isinstance(contenu, dict):
            contenu = contenu.get(d, {})

    if st.session_state.chemin:
        st.markdown('<div class="btn-retour">', unsafe_allow_html=True)
        if st.button("⬅️ ON REVIENT !"): 
            st.session_state.chemin.pop()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    titre = st.session_state.chemin[-1] if st.session_state.chemin else "MONDE MAGIQUE"
    st.markdown(f"<h1 class='titre-enfant'>✨ {titre}</h1>", unsafe_allow_html=True)
    
    if isinstance(contenu, dict):
        for k, v in contenu.items():
            if isinstance(v, dict):
                st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
                if st.button(k): 
                    st.session_state.chemin.append(k)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
                if st.button(k): parler(v)
                st.markdown('</div>', unsafe_allow_html=True)
