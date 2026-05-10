import streamlit as st
from gtts import gTTS
import base64
import io
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MONDE MAGIQUE 🎈", layout="wide", initial_sidebar_state="collapsed")

# Récupération de la clé Mistral dans les Secrets
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
except Exception as e:
    st.error(f"Oups ! Il manque des fichiers dans le dossier univers.")
    ECOLE_DATA = NATURE_DATA = MONDE_DATA = JEUX_DATA = {}

# --- 3. LOGIQUE IA SÉCURISÉE (MISTRAL) ---
def demander_au_doudou(question):
    if not MISTRAL_API_KEY:
        return "Oh non ! Mon cerveau magique n'est pas branché."
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    
    # LE VERROU DE SÉCURITÉ : On définit le rôle strict de l'IA ici
    data = {
        "model": "mistral-tiny",
        "messages": [
            {
                "role": "system", 
                "content": """Tu es un doudou magique protecteur pour de très jeunes enfants (2-5 ans). 
                CONSIGNES DE SÉCURITÉ :
                1. Utilise un langage doux, joyeux et extrêmement poli.
                2. INTERDICTION TOTALE d'utiliser des mots vulgaires, violents ou complexes.
                3. Si l'enfant pose une question inappropriée ou méchante, réponds : 'Oh, restons gentils comme des petits chats ! Dis-moi quelque chose de doux.'
                4. Fais des phrases très courtes (max 15 mots)."""
            },
            {"role": "user", "content": question}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Je fais un petit dodo, reviens plus tard mon petit chou !"

# --- 4. DESIGN ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .stApp {{ 
        background: linear-gradient(-45deg, #FFD6E8, #C9F2FF, #D8FFF1, #FFF2B2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }}
    @keyframes gradient {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    
    .titre-enfant {{ text-align: center; color: #8A63FF !important; font-size: 40px; font-family: 'Fredoka One', cursive; text-shadow: 2px 2px 0px #FFFFFF; }}
    
    /* Boutons de Navigation (Haut) */
    .btn-nav button {{
        background: #FFFFFF !important;
        border: 3px solid #8A63FF !important;
        border-radius: 20px !important;
        color: #8A63FF !important;
        font-family: 'Fredoka One', cursive !important;
        font-size: 18px !important;
        height: 60px !important;
        width: 100% !important;
    }}

    /* Boutons Dossiers (Jaunes avec texte) */
    .btn-dossier button {{ 
        background: #FFF2B2 !important; 
        border: 5px solid #FFCC00 !important; 
        height: 100px !important; 
        border-radius: 30px !important; 
        color: #D35400 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 22px !important;
        box-shadow: 0px 6px 0px #FFB300 !important; 
        margin-bottom:10px; 
        width: 100% !important; 
    }}
    
    /* Boutons Objets (Blancs avec texte) */
    .btn-objet button {{ 
        background: white !important; 
        height: 80px !important; 
        border-radius: 25px !important; 
        color: #2C3E50 !important; 
        font-family: 'Fredoka One', cursive !important; 
        font-size: 20px !important;
        margin-bottom:10px; 
        border: 3px solid #EEE !important; 
        width: 100% !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

def parler(txt):
    tts = gTTS(text=str(txt), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# --- 5. ÉTATS ET NAVIGATION ---
if 'mode' not in st.session_state: st.session_state.mode = "jeu"
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'chemin' not in st.session_state: st.session_state.chemin = []

# Barre d'outils du haut (Modifiée avec Texte + Dessin)
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
with c1:
    if st.button("📚 ÉCOLE", key="nav_1"):
        st.session_state.mode = "jeu"
        st.session_state.slide = 1
        st.session_state.chemin = []
with c2: 
    if st.button("🧮 CALCULS", key="nav_calc"): st.session_state.mode = "calc"
with c3: 
    if st.button("📖 MOTS", key="nav_dict"): st.session_state.mode = "dict"
with c4: 
    if st.button("🤖 DOUDOU IA", key="nav_ia"): st.session_state.mode = "ia"

st.write("---") # Petite séparation

# --- AFFICHAGE ---
if st.session_state.mode == "calc":
    st.markdown("<h1 class='titre-enfant'>Ma Calculatrice 🧮</h1>", unsafe_allow_html=True)
    n = st.number_input("Choisis un nombre :", 0, 10)
    if st.button("ÉCOUTER LE NOMBRE"): parler(n)

elif st.session_state.mode == "dict":
    st.markdown("<h1 class='titre-enfant'>Mes Jolis Mots 📖</h1>", unsafe_allow_html=True)
    mot = st.text_input("Écris un mot ici :")
    if mot: parler(f"C'est le mot {mot} !")

elif st.session_state.mode == "ia":
    st.markdown("<h1 class='titre-enfant'>Doudou IA 🤖</h1>", unsafe_allow_html=True)
    st.write("Pose une question gentille à ton doudou !")
    question = st.text_input("Ta question :")
    if st.button("PARLER AU DOUDOU"):
        rep = demander_au_doudou(question)
        st.info(rep)
        parler(rep)

else:
    # Navigation des univers (Lions, Monde, Cadeaux)
    cols = st.columns(3)
    titles = ["🦁 NATURE", "🌍 MONDE", "🎁 JEUX"]
    for i, title in enumerate(titles):
        if cols[i].button(title, key=f"subnav_{i}"):
            st.session_state.slide = i + 2
            st.session_state.chemin = []
            st.rerun()

    mapping = {1: ECOLE_DATA, 2: NATURE_DATA, 3: MONDE_DATA, 4: JEUX_DATA}
    contenu = mapping[st.session_state.slide]
    for d in st.session_state.chemin: contenu = contenu[d]

    if st.session_state.chemin:
        if st.button("⬅️ RETOUR"):
            st.session_state.chemin.pop()
            st.rerun()

    st.markdown(f"<h1 class='titre-enfant'>{'✨ ' + st.session_state.chemin[-1] if st.session_state.chemin else 'MONDE MAGIQUE'}</h1>", unsafe_allow_html=True)
    
    # Boutons avec Texte
    if isinstance(contenu, dict):
        for k, v in contenu.items():
            if isinstance(v, dict):
                st.markdown('<div class="btn-dossier">', unsafe_allow_html=True)
                if st.button(k): 
                    st.session_state.chemin.append(k)
                    st.rerun()
            else:
                st.markdown('<div class="btn-objet">', unsafe_allow_html=True)
                if st.button(k): parler(v)
