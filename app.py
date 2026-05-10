import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- 1. CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="L'Empire des Petits Génies", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

# --- 2. DESIGN "ULTRA-FLUIDE MOBILE" ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background: linear-gradient(135deg, #FFF5FD 0%, #E7F0FD 100%); }
    
    /* Boutons de navigation et de jeux */
    .stButton > button {
        width: 100%; height: 95px !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 25px !important; border: 3px solid white !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.08) !important;
        transition: 0.1s !important; background-color: white;
        color: #333 !important;
    }
    .stButton > button:active { transform: scale(0.95); background-color: #F0F2F6 !important; }
    
    .big-title { text-align: center; color: #FF6B6B; font-size: 40px !important; font-weight: 900; margin-bottom: 20px; }
    .display-card {
        background: white; border-radius: 35px; padding: 25px;
        text-align: center; border: 6px solid #FFD1DC; font-size: 45px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LA GIGA-BASE DE DONNÉES ---
DATABASE = {
    "🌍 Drapeaux": {
        "Europe": {"🇫🇷":"France","🇧🇪":"Belgique","🇨🇭":"Suisse","🇮🇹":"Italie","🇪🇸":"Espagne","🇩🇪":"Allemagne","🇬🇧":"Royaume-Uni","🇵🇹":"Portugal","🇳🇱":"Pays-Bas","🇮🇪":"Irlande","🇬🇷":"Grèce","🇦🇹":"Autriche"},
        "Afrique": {"🇲🇦":"Maroc","🇩🇿":"Algérie","🇹🇳":"Tunisie","🇸🇳":"Sénégal","🇨🇮":"Côte d'Ivoire","🇨🇲":"Cameroun","🇲🇱":"Mali","🇨🇬":"Congo","🇪🇬":"Égypte","🇿🇦":"Afrique du Sud"},
        "Amériques": {"🇨🇦":"Canada","🇺🇸":"États-Unis","🇲🇽":"Mexique","🇧🇷":"Brésil","🇦🇷":"Argentine","🇨🇴":"Colombie","🇨🇱":"Chili","🇵🇪":"Pérou"},
        "Asie/Océanie": {"🇯🇵":"Japon","🇨🇳":"Chine","🇰🇷":"Corée","🇮🇳":"Inde","🇦🇺":"Australie","🇹🇭":"Thaïlande","🇻🇳":"Vietnam","🇸🇬":"Singapour"}
    },
    "🦁 Animaux": {
        "Savane/Jungle": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🐯":"Tigre","🐵":"Singe","🦛":"Hippo","🦏":"Rhino"},
        "Mer": {"🐬":"Dauphin","🐋":"Baleine","🦈":"Requin","🐙":"Poulpe","🦀":"Crabe","🐢":"Tortue","🐠":"Poisson","🦐":"Crevette"},
        "Ferme": {"🐮":"Vache","🐷":"Cochon","🐔":"Poule","🦆":"Canard","🐴":"Cheval","🐑":"Mouton","🐰":"Lapin","🐐":"Chèvre"},
        "Dinosaures": {"🦖":"T-Rex","🦕":"Diplodocus","🕊️":"Ptérodactyle","🐢":"Tricératops"}
    },
    "🍎 Le Marché": {
        "Fruits": {"🍎":"Pomme","🍌":"Banane","🍓":"Fraise","🍉":"Pastèque","🍍":"Ananas","🥝":"Kiwi","🍒":"Cerise","🍑":"Pêche","🍇":"Raisin"},
        "Légumes": {"Carotte":"🥕","Brocoli":"🥦","Maïs":"🌽","Tomate":"🍅","Aubergine":"🍆","Poivron":"🫑","Oignon":"🧅","🥔":"Patate"}
    },
    "🏠 Maison": {
        "Objets": {"🛌":"Lit","🛋️":"Canapé","🛀":"Bain","📺":"Télé","🔑":"Clé","🍽️":"Assiette","🧸":"Jouet","🚲":"Vélo"},
        "Le Corps": {"👀":"Yeux","👂":"Oreilles","👃":"Nez","👄":"Bouche","🖐️":"Main","🦶":"Pied","💪":"Bras"}
    },
    "🚀 Transports": {"🚗":"Voiture","🚒":"Pompier","🚑":"Ambulance","🚓":"Police","✈️":"Avion","🚀":"Fusée","🚜":"Tracteur","🚢":"Bateau","🚁":"Hélicoptère"},
    "🛠️ Métiers": {"🧑‍🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🧑‍🚀":"Astronaute","🧑‍🍳":"Cuisinier","🧑‍🌾":"Fermier"}
}

# --- 4. LOGIQUE AUDIO & NAV ---
if 'page' not in st.session_state: st.session_state.page = "menu"
if 'sub_page' not in st.session_state: st.session_state.sub_page = ""
if 'lang' not in st.session_state: st.session_state.lang = "fr"
if 'stars' not in st.session_state: st.session_state.stars = 0

def parler(txt):
    if not txt: return
    try:
        tts = gTTS(text=str(txt), lang=st.session_state.lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def nav(p, sub=""):
    st.session_state.page = p
    st.session_state.sub_page = sub
    st.rerun()

# --- 5. INTERFACE UTILISATEUR ---

# 🏠 MENU PRINCIPAL
if st.session_state.page == "menu":
    st.markdown("<h1 class='big-title'>👑 L'EMPIRE DES BÉBÉS</h1>", unsafe_allow_html=True)
    
    # Sélecteur de langue discret
    st.session_state.lang = st.radio("Langue / Language", ["fr", "en", "es"], horizontal=True)
    
    cols = st.columns(2)
    categories = list(DATABASE.keys()) + ["🔤 Alphabet", "🔢 Chiffres", "➕ Maths", "❓ Quiz"]
    
    for i, cat in enumerate(categories):
        with cols[i % 2]:
            if st.button(cat):
                if cat in DATABASE: nav(cat)
                elif "Maths" in cat: nav("maths")
                else: nav(cat.split()[-1].lower())

# 🔤 ALPHABET
elif st.session_state.page == "alphabet":
    if st.button("⬅️ Menu"): nav("menu")
    st.title("🔤 Alphabet")
    cols = st.columns(4)
    for i, l in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        with cols[i % 4]:
            if st.button(l): parler(l)

# 🔢 CHIFFRES (0 à 100)
elif st.session_state.page == "chiffres":
    if st.button("⬅️ Menu"): nav("menu")
    st.title("🔢 Chiffres (0-100)")
    cols = st.columns(4)
    for i in range(101):
        with cols[i % 4]:
            if st.button(str(i)): parler(i)

# ➕ MATHÉMATIQUES
elif st.session_state.page == "maths":
    if st.button("⬅️ Menu"): nav("menu")
    st.title("➕ Mes Premiers Calculs")
    calc = [("1+1", "2"), ("2+2", "4"), ("5+5", "10"), ("10-1", "9"), ("3+2", "5")]
    for q, r in calc:
        if st.button(f"{q} = ?"): parler(f"{q} égale {r}")

# ❓ QUIZ
elif st.session_state.page == "quiz":
    if st.button("⬅️ Menu"): nav("menu")
    st.title("🎯 Trouve l'image !")
    st.info("Bientôt : Système de quiz automatique sur toute la base de données !")

# 🌍 NAVIGATION DYNAMIQUE (Drapeaux, Animaux, etc.)
elif st.session_state.page in DATABASE:
    if st.button("⬅️ Menu"): nav("menu")
    st.title(st.session_state.page)
    
    data_cat = DATABASE[st.session_state.page]
    
    # Si c'est un dictionnaire de sous-catégories (ex: Europe, Afrique...)
    if isinstance(list(data_cat.values())[0], dict):
        if st.session_state.sub_page == "":
            cols = st.columns(2)
            for i, sub in enumerate(data_cat.keys()):
                with cols[i % 2]:
                    if st.button(sub):
                        st.session_state.sub_page = sub
                        st.rerun()
        else:
            if st.button(f"⬅️ Retour {st.session_state.page}"):
                st.session_state.sub_page = ""
                st.rerun()
            
            st.markdown(f"<div class='display-card'>{st.session_state.sub_page}</div>", unsafe_allow_html=True)
            items = data_cat[st.session_state.sub_page]
            cols = st.columns(2)
            for i, (e, n) in enumerate(items.items()):
                with cols[i % 2]:
                    if st.button(f"{e}\n{n}"): parler(n)
    
    # Si c'est une catégorie directe (ex: Transports, Métiers)
    else:
        cols = st.columns(2)
        for i, (e, n) in enumerate(data_cat.items()):
            with cols[i % 2]:
                if st.button(f"{e}\n{n}"): parler(n)

# --- 6. SIDEBAR ADMIN ---
with st.sidebar:
    st.write("### ⚙️ Mode Parent")
    if st.text_input("Code", type="password") == "admin":
        st.success("Accès OK")
        st.write(f"Étoiles gagnées : {st.session_state.stars}")
