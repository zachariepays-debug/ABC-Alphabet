import streamlit as st
from gtts import gTTS
import base64
import io

# --- CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="L'Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- DESIGN "ULTRA-CONTRASTE & GÉANT" ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000000; } 
    
    .stButton > button {
        width: 100%; height: 110px !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 25px !important;
        border: 4px solid #ffffff !important;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    /* Couleurs Electriques */
    div[data-testid="stVerticalBlock"] > div:nth-child(odd) button { background: #00FFCC !important; color: #000 !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(even) button { background: #FF00FF !important; color: #fff !important; }
    
    .titre-giga {
        text-align: center; color: #00FFCC; font-size: 60px !important; 
        font-weight: 900; text-shadow: 4px 4px #FF00FF; margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LA MINE D'OR ABSOLUE (DATA) ---
DATABASE = {
    "🦖 Dinosaures": {
        "Carnivores": {"🦖 T-Rex":"Tyrannosaure","🦖 Raptor":"Vélociraptor","🦖 Spino":"Spinosaure","🦖 Carno":"Carnotaure"},
        "Herbivores": {"🦕 Diplo":"Diplodocus","🦕 Tricé":"Tricératops","🦕 Stego":"Stégosaure","🦕 Brachio":"Brachiosaure"},
        "Ciel & Mer": {"🕊️ Ptéro":"Ptérodactyle","🌊 Mosa":"Mosasaurus","🌊 Plésio":"Plésiosaure"}
    },
    "🦁 Tous les Animaux": {
        "Savane & Jungle": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🐯":"Tigre","🐵":"Singe","🦛":"Hippopotame","🦏":"Rhinocéros","🐆":"Léopard","🦍":"Gorille"},
        "Banquise & Froid": {"🐻‍❄️":"Ours Polaire","🐧":"Manchot","🦭":"Phoque","🦌":"Renne","🐺":"Loup"},
        "Insectes": {"🦋":"Papillon","🐝":"Abeille","🐞":"Coccinelle","🐜":"Fourmi","🕷️":"Araignée","🦗":"Criquet"}
    },
    "🧑‍🔧 Métiers": {
        "Secours": {"🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🚑":"Ambulancier","🚁":"Sauveteur"},
        "Quotidien": {"🧑‍🍳":"Cuisinier","🧑‍🌾":"Fermier","🧑‍🏫":"Maître d'école","🧑‍🔧":"Mécanicien","🥖":"Boulanger","👷":"Maçon"},
        "Rêves": {"🧑‍🚀":"Astronaute","🧑‍✈️":"Pilote","🎸":"Musicien","🎨":"Peintre","🕵️":"Détective"}
    },
    "🔢 Maths & Formes": {
        "Chiffres": {str(i):str(i) for i in range(101)},
        "Formes": {"🟦":"Carré","🔴":"Rond","🔺":"Triangle","⭐":"Étoile","💎":"Losange","❤️":"Cœur"},
        "Calculs": {"1+1=2":"Un plus un égale deux","2+2=4":"Deux plus deux égale quatre","5+5=10":"Cinq plus cinq égale dix"}
    },
    "🚀 Transports": {
        "Gros Engins": {"🚜":"Tracteur","🏗️":"Grue","🚛":"Camion","🚛":"Remorque","🧹":"Balayeuse"},
        "Vitesse": {"🏎️":"Formule 1","🚄":"Train Rapide","🚀":"Fusée","✈️":"Avion de chasse"}
    }
}

# --- LOGIQUE FONCTIONNELLE ---
if 'page' not in st.session_state: st.session_state.page = "menu"
if 'sub' not in st.session_state: st.session_state.sub = ""

def parler(txt):
    try:
        tts = gTTS(text=str(txt), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def nav(p, s=""):
    st.session_state.page = p
    st.session_state.sub = s
    st.rerun()

# --- INTERFACE ---

if st.session_state.page == "menu":
    st.markdown("<h1 class='titre-giga'>EMPIRE GÉNIE</h1>", unsafe_allow_html=True)
    cols = st.columns(2)
    options = list(DATABASE.keys()) + ["🔤 Alphabet"]
    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt):
                if opt in DATABASE: nav(opt)
                else: nav("alphabet")

elif st.session_state.page in DATABASE:
    if st.button("⬅️ MENU"): nav("menu")
    st.markdown(f"<h1 style='color:white; text-align:center;'>{st.session_state.page}</h1>", unsafe_allow_html=True)
    
    content = DATABASE[st.session_state.page]
    
    if st.session_state.sub == "":
        cols = st.columns(2)
        for i, sub_cat in enumerate(content.keys()):
            with cols[i % 2]:
                if st.button(sub_cat): nav(st.session_state.page, sub_cat)
    else:
        if st.button("⬅️ RETOUR"): nav(st.session_state.page, "")
        st.markdown(f"<h2 style='color:#00FFCC; text-align:center;'>{st.session_state.sub}</h2>", unsafe_allow_html=True)
        items = content[st.session_state.sub]
        cols = st.columns(2)
        for i, (key, val) in enumerate(items.items()):
            with cols[i % 2]:
                if st.button(f"{key}\n{val}"): parler(val)

elif st.session_state.page == "alphabet":
    if st.button("⬅️ MENU"): nav("menu")
    st.markdown("<h1 style='color:white; text-align:center;'>🔤 L'ALPHABET</h1>", unsafe_allow_html=True)
    cols = st.columns(4)
    for i, l in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        with cols[i % 4]:
            if st.button(l): parler(l)
