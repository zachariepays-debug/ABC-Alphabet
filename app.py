import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="L'Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- DESIGN "PREMIUM DARK" ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #050505; } 
    
    /* Animation de pulsation */
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }

    .stButton > button {
        width: 100%; height: 100px !important;
        font-size: 20px !important; font-weight: 900 !important;
        border-radius: 25px !important; border: 3px solid #333 !important;
        text-transform: uppercase; animation: pulse 4s infinite; transition: 0.2s;
    }
    
    /* Navigation Dots Actifs */
    .nav-container { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
    .dot-btn { 
        height: 20px; width: 20px; border-radius: 50%; border: none; cursor: pointer; 
        transition: 0.3s; box-shadow: 0 0 10px rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ÉTATS ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'page' not in st.session_state: st.session_state.page = "home"
if 'sub' not in st.session_state: st.session_state.sub = ""

# --- FONCTIONS ---
def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def changer_slide(n):
    st.session_state.slide = n
    st.session_state.page = "home"
    st.rerun()

def nav(p, s=""):
    st.session_state.page = p
    st.session_state.sub = s
    st.rerun()

# --- GIGA BASE DE DONNÉES ---
DATABASE = {
    "SLIDE_1": { # APPRENTISSAGE
        "🔤 Alphabet": { "Lettres": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") },
        "🔢 Chiffres": { "Compter": [str(i) for i in range(101)] },
        "📐 Formes": { "Géométrie": {"🟦":"Carré","🔴":"Rond","🔺":"Triangle","⭐":"Étoile","💎":"Losange","❤️":"Cœur"} },
        "➕ Maths": { "Calculs": {"1+1=2":"2","2+2=4":"4","5+5=10":"10","10+10=20":"20"} }
    },
    "SLIDE_2": { # NATURE
        "🦖 Dinosaures": {
            "Carnivores": {"🦖 T-Rex":"Tyrannosaure","🦖 Raptor":"Vélociraptor","🦖 Spino":"Spinosaure"},
            "Herbivores": {"🦕 Diplo":"Diplodocus","🦕 Tricé":"Tricératops","🦕 Stego":"Stégosaure"}
        },
        "🦁 Animaux": {
            "Savane": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🦛":"Hippo"},
            "Mer": {"🐬":"Dauphin","🐋":"Baleine","🦈":"Requin","🐙":"Poulpe","🐢":"Tortue"},
            "Forêt": {"🦊":"Renard","🦌":"Cerf","🐺":"Loup","🐻":"Ours","🐿️":"Écureuil"}
        },
        "🪐 Espace": { "Galaxie": {"☀️":"Soleil","🌍":"Terre","🌙":"Lune","🪐":"Saturne","🚀":"Fusée"} }
    },
    "SLIDE_3": { # MONDE
        "🌍 Drapeaux": {
            "Afrique": {"🇲🇦":"Maroc","🇩🇿":"Algérie","🇹🇳":"Tunisie","🇸🇳":"Sénégal","🇨🇮":"Côte d'Ivoire"},
            "Europe": {"🇫🇷":"France","🇧🇪":"Belgique","🇨🇭":"Suisse","🇮🇹":"Italie","🇪🇸":"Espagne"},
            "Amériques": {"🇨🇦":"Canada","🇺🇸":"États-Unis","🇲🇽":"Mexique","🇧🇷":"Brésil"}
        },
        "🚒 Métiers": { "Travail": {"🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🧑‍🍳":"Chef","🧑‍🚀":"Astronaute"} },
        "🚀 Transports": { "Véhicules": {"🚗":"Voiture","🚒":"Pompier","✈️":"Avion","🚜":"Tracteur","🚢":"Bateau"} }
    }
}

# --- BARRE DE NAVIGATION (LES 3 BOUTONS) ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,1,1])
with c1: 
    color = "#FF0055" if st.session_state.slide == 1 else "#333"
    if st.button("●", key="dot1", help="Apprentissage"): changer_slide(1)
with c2: 
    color = "#FF0055" if st.session_state.slide == 2 else "#333"
    if st.button("●", key="dot2", help="Nature"): changer_slide(2)
with c3: 
    color = "#FF0055" if st.session_state.slide == 3 else "#333"
    if st.button("●", key="dot3", help="Monde"): changer_slide(3)
st.markdown('</div>', unsafe_allow_html=True)

# --- AFFICHAGE DU CONTENU ---
current_db = DATABASE[f"SLIDE_{st.session_state.slide}"]

if st.session_state.page == "home":
    st.markdown(f"<h1 style='text-align:center; color:white;'>UNIVERS {st.session_state.slide}</h1>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, cat in enumerate(current_db.keys()):
        with cols[i % 2]:
            if st.button(cat, key=f"cat_{cat}"): nav(cat)

elif st.session_state.page in current_db:
    if st.button("⬅️ RETOUR"): nav("home")
    st.markdown(f"<h2 style='text-align:center; color:#FF0055;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
    
    sub_data = current_db[st.session_state.page]
    
    if st.session_state.sub == "":
        cols = st.columns(2)
        for i, s in enumerate(sub_data.keys()):
            with cols[i % 2]:
                if st.button(s, key=f"sub_{s}"): nav(st.session_state.page, s)
    else:
        if st.button("⬅️"): nav(st.session_state.page, "")
        items = sub_data[st.session_state.sub]
        cols = st.columns(2)
        
        # Gestion spécifique Alphabet/Chiffres (listes) vs Reste (dict)
        if isinstance(items, list):
            for i, val in enumerate(items):
                with cols[i % 2]:
                    if st.button(val, key=f"item_{val}_{i}"): parler(val)
        else:
            for i, (k, v) in enumerate(items.items()):
                with cols[i % 2]:
                    if st.button(f"{k}\n{v}", key=f"item_{v}_{i}"): parler(v)
