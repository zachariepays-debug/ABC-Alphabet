import streamlit as st
from gtts import gTTS
import base64
import io
import random

# --- 1. CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS "MOBILE-OPTIMIZED" (PLUS GROS, PLUS FLUIDE) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #000000; } 
    
    /* Adaptation Mobile : Boutons énormes et centrés */
    .stButton > button {
        width: 100% !important;
        height: 90px !important;
        margin-bottom: 15px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        border: 4px solid #ffffff33 !important;
        text-transform: uppercase;
        color: white !important;
        transition: 0.1s;
    }
    
    /* Effet de clic tactile */
    .stButton > button:active {
        transform: scale(0.95);
        background-color: #fff !important;
        color: #000 !important;
    }

    /* Couleurs Vibrantes */
    div[data-testid="stVerticalBlock"] > div:nth-child(4n+1) button { background: linear-gradient(90deg, #FF0055, #FF5588) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(4n+2) button { background: linear-gradient(90deg, #00CCFF, #0077FF) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(4n+3) button { background: linear-gradient(90deg, #00FFCC, #00AB8E) !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(4n+4) button { background: linear-gradient(90deg, #FFCC00, #FF9900) !important; }

    .nav-bar {
        display: flex; justify-content: center; gap: 8px; padding: 10px;
        background: #111; border-radius: 50px; margin-bottom: 20px;
        position: sticky; top: 0; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÉTATS ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'page' not in st.session_state: st.session_state.page = "home"
if 'sub' not in st.session_state: st.session_state.sub = ""

# --- 4. FONCTIONS ---
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
    st.session_state.sub = ""
    st.rerun()

# --- 5. GIGA DATA ---
DATABASE = {
    "SLIDE_1": { # ÉCOLE
        "🔤 Alphabet": {"Lettres": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")},
        "🔢 Chiffres": {"Compter": [str(i) for i in range(101)]},
        "📐 Formes": {"Géométrie": {"🟦":"Carré","🔴":"Rond","🔺":"Triangle","⭐":"Étoile","💎":"Losange","❤️":"Cœur"}},
        "🎨 Couleurs": {"Nuances": {"🔴":"Rouge","🔵":"Bleu","🟢":"Vert","🟡":"Jaune","🟠":"Orange","🟣":"Violet","⚫":"Noir","⚪":"Blanc"}}
    },
    "SLIDE_2": { # NATURE & DINOS
        "🦖 Dinosaures": {
            "Carnivores": {"🦖 T-Rex":"Tyrannosaure","🦖 Raptor":"Vélociraptor","🦖 Spino":"Spinosaure","🦖 Allosaure":"Allosaure"},
            "Herbivores": {"🦕 Diplo":"Diplodocus","🦕 Tricé":"Tricératops","🦕 Stego":"Stégosaure","🦕 Brachio":"Brachiosaure"}
        },
        "🦁 Animaux": {
            "Savane": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🐵":"Singe","🦛":"Hippo"},
            "Océan": {"🐬":"Dauphin","🐋":"Baleine","🦈":"Requin","🐙":"Poulpe","🐢":"Tortue","🦀":"Crabe"},
            "Ferme": {"🐮":"Vache","🐷":"Cochon","🐔":"Poule","🦆":"Canard","🐴":"Cheval","🐑":"Mouton"}
        }
    },
    "SLIDE_3": { # MONDE & HUMAINS
        "🌍 Drapeaux": {
            "Monde": {"🇫🇷":"France","🇲🇦":"Maroc","🇩🇿":"Algérie","🇹🇳":"Tunisie","🇸🇳":"Sénégal","🇨🇮":"Côte d'Ivoire","🇧🇪":"Belgique","🇨🇭":"Suisse","🇮🇹":"Italie","🇪🇸":"Espagne","🇺🇸":"USA","🇧🇷":"Brésil","🇯🇵":"Japon"}
        },
        "🚀 Transports": {
            "Ville": {"🚗":"Voiture","🚓":"Police","🚒":"Pompier","🚑":"Ambulance","🚌":"Bus","🚜":"Tracteur"},
            "Air & Mer": {"✈️":"Avion","🚀":"Fusée","🚁":"Hélicoptère","🚢":"Bateau","🛸":"Soucoupe"}
        },
        "🧑‍⚕️ Métiers": {"Travail": {"🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🧑‍🍳":"Chef","🧑‍🚀":"Astronaute","🧑‍🏫":"Maître"}}
    },
    "SLIDE_4": { # JEUX & MAGIE
        "🎹 Musique": {"Instruments": {"🎹":"Piano","🎸":"Guitare","🥁":"Batterie","🎺":"Trompette","🎻":"Violon"}},
        "😊 Émotions": {"Humeur": {"😀":"Content","😢":"Triste","😡":"En Colère","😱":"Peur","😴":"Dodo"}},
        "🏆 Récompenses": {
            "Magie": {
                "🎁 CADEAU": "Confettis",
                "🪄 MAGIE": "Neige",
                "🎈 BALLONS": "Ballons",
                "🌟 ÉTOILE": "Bravo"
            }
        }
    }
}

# --- 6. NAVIGATION (LES POINTS) ---
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
cols = st.columns(4)
icons = ["📚", "🦁", "🌍", "🎁"]
for i in range(4):
    with cols[i]:
        label = f"{icons[i]}"
        if st.session_state.slide == i+1: label = "●"
        if st.button(label, key=f"dot_{i}"): changer_slide(i+1)
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. LOGIQUE D'AFFICHAGE ---
current_db = DATABASE[f"SLIDE_{st.session_state.slide}"]

if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center; color:white;'>EMPIRE DES GÉNIES</h1>", unsafe_allow_html=True)
    for cat in current_db.keys():
        if st.button(cat):
            st.session_state.page = cat
            st.rerun()

else:
    if st.button("⬅️ RETOUR"):
        st.session_state.page = "home"
        st.session_state.sub = ""
        st.rerun()
    
    st.markdown(f"<h2 style='text-align:center; color:white;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
    sub_data = current_db[st.session_state.page]
    
    if st.session_state.sub == "":
        for s in sub_data.keys():
            if st.button(s):
                st.session_state.sub = s
                st.rerun()
    else:
        if st.button("⬅️ PRÉCÉDENT"):
            st.session_state.sub = ""
            st.rerun()
            
        items = sub_data[st.session_state.sub]
        for k, v in (items.items() if isinstance(items, dict) else enumerate(items)):
            label = f"{k} {v}" if isinstance(items, dict) else v
            if st.button(label):
                parler(v if isinstance(items, dict) else v)
                
                # --- SYSTÈME DE RÉCOMPENSES UNIQUES ---
                if "CADEAU" in label: st.snow() # Ici on détourne snow pour faire un effet "pluie"
                if "MAGIE" in label: st.snow()
                if "BALLONS" in label: st.balloons()
                if "ÉTOILE" in label: st.balloons()
