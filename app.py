import streamlit as st
from gtts import gTTS
import base64
import io
import random
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="L'Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS ANIMÉ & CONTRASTE MAXIMAL ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #0a0a0a; } 
    
    /* Animations CSS */
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-5px); } 100% { transform: translateY(0px); } }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }

    .stButton > button {
        width: 100%; height: 110px !important;
        font-size: 22px !important; font-weight: 900 !important;
        border-radius: 20px !important; border: 3px solid #444 !important;
        text-transform: uppercase; 
        animation: float 4s infinite ease-in-out, slideIn 0.4s ease-out;
        transition: all 0.2s;
    }
    .stButton > button:active { transform: scale(0.9) !important; border-color: #FFF !important; }
    
    /* Couleurs des boutons */
    div[data-testid="stVerticalBlock"] > div:nth-child(odd) button { background: linear-gradient(135deg, #FF0055, #FF5588) !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(even) button { background: linear-gradient(135deg, #00CCFF, #0077FF) !important; color: white !important; }
    
    /* Titres et Navigation */
    .titre-page { text-align: center; color: #FFD700; font-size: 45px !important; font-weight: 900; text-shadow: 2px 2px #FF0055; margin-bottom: 20px; animation: slideIn 0.5s; }
    .nav-box { display: flex; justify-content: center; gap: 15px; margin-bottom: 25px; background: #1a1a1a; padding: 15px; border-radius: 30px; border: 2px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÉTATS DE L'APPLICATION ---
if 'slide' not in st.session_state: st.session_state.slide = 1
if 'page' not in st.session_state: st.session_state.page = "home"
if 'sub' not in st.session_state: st.session_state.sub = ""

# --- 4. MOTEUR AUDIO ---
def parler(txt):
    if not txt: return
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

def nav(p, s=""):
    st.session_state.page = p
    st.session_state.sub = s
    st.rerun()

# --- 5. LA BASE DE DONNÉES "CARTE BLANCHE" (0 à 1000) ---
DATABASE = {
    "SLIDE_1": { # 📚 L'ÉCOLE
        "🔤 Alphabet": { "Lettres": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") },
        "🔢 Chiffres": { "0 à 50": [str(i) for i in range(51)], "50 à 100": [str(i) for i in range(51, 101)] },
        "📐 Formes": { "Géométrie": {"🟦":"Carré","🔴":"Rond","🔺":"Triangle","⭐":"Étoile","💎":"Losange","❤️":"Cœur","🟩":"Rectangle"} },
        "➕ Calculs": { "Additions": {"1+1=2":"2","2+2=4":"4","5+5=10":"10","10+10=20":"20"}, "Soustractions": {"2-1=1":"1","5-2=3":"3","10-5=5":"5"} }
    },
    "SLIDE_2": { # 🦁 NATURE & ANIMAUX
        "🦖 Dinosaures": {
            "Carnivores": {"🦖 T-Rex":"Tyrannosaure","🦖 Raptor":"Vélociraptor","🦖 Spino":"Spinosaure"},
            "Herbivores": {"🦕 Diplo":"Diplodocus","🦕 Tricé":"Tricératops","🦕 Stego":"Stégosaure","🦕 Brachio":"Brachiosaure"},
            "Volants & Marins": {"🕊️ Ptéro":"Ptérodactyle","🌊 Mosa":"Mosasaurus"}
        },
        "🦁 Zoo du Monde": {
            "Savane & Jungle": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🐵":"Singe","🦛":"Hippo","🦏":"Rhino","🐆":"Léopard","🦍":"Gorille","🐯":"Tigre"},
            "Océan": {"🐬":"Dauphin","🐋":"Baleine","🦈":"Requin","🐙":"Poulpe","🐢":"Tortue","🦀":"Crabe","🦞":"Homard","🐠":"Poisson","🐡":"Poisson lune"},
            "Ferme & Maison": {"🐮":"Vache","🐷":"Cochon","🐔":"Poule","🦆":"Canard","🐴":"Cheval","🐑":"Mouton","🐰":"Lapin","🐶":"Chien","🐱":"Chat"}
        },
        "🐞 Insectes": { "Petites Bêtes": {"🦋":"Papillon","🐝":"Abeille","🐞":"Coccinelle","🐜":"Fourmi","🕷️":"Araignée","🐛":"Chenille","🐌":"Escargot"} }
    },
    "SLIDE_3": { # 🌍 LE MONDE DES HOMMES
        "🌍 Drapeaux": {
            "Europe": {"🇫🇷":"France","🇧🇪":"Belgique","🇨🇭":"Suisse","🇮🇹":"Italie","🇪🇸":"Espagne","🇩🇪":"Allemagne","🇬🇧":"Angleterre","🇵🇹":"Portugal","🇳🇱":"Pays-Bas","🇬🇷":"Grèce","🇷🇺":"Russie","🇸🇪":"Suède"},
            "Afrique": {"🇲🇦":"Maroc","🇩🇿":"Algérie","🇹🇳":"Tunisie","🇸🇳":"Sénégal","🇨🇮":"Côte d'Ivoire","🇨🇲":"Cameroun","🇲🇱":"Mali","🇪🇬":"Égypte","🇿🇦":"Afrique du Sud","🇲🇬":"Madagascar"},
            "Amériques": {"🇨🇦":"Canada","🇺🇸":"États-Unis","🇲🇽":"Mexique","🇧🇷":"Brésil","🇦🇷":"Argentine","🇨🇴":"Colombie","🇨🇱":"Chili","🇵🇪":"Pérou","🇨🇺":"Cuba"},
            "Asie & Océanie": {"🇯🇵":"Japon","🇨🇳":"Chine","🇰🇷":"Corée","🇮🇳":"Inde","🇦🇺":"Australie","🇹🇭":"Thaïlande","🇻🇳":"Vietnam"}
        },
        "🚀 Transports": {
            "Sur Terre": {"🚗":"Voiture","🚓":"Police","🚒":"Pompier","🚑":"Ambulance","🚌":"Bus","🚜":"Tracteur","🚂":"Train","🚲":"Vélo","🏍️":"Moto"},
            "Air & Eau": {"✈️":"Avion","🚀":"Fusée","🚁":"Hélicoptère","🚢":"Bateau","🛶":"Canoë","🛳️":"Paquebot"}
        },
        "🧑‍⚕️ Métiers": { "Au travail": {"🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🧑‍🍳":"Cuisinier","🧑‍🚀":"Astronaute","🧑‍🏫":"Professeur","🧑‍🔧":"Mécanicien","🧑‍🌾":"Fermier","👩‍⚖️":"Juge"} }
    },
    "SLIDE_4": { # 🧠 LE COIN DES CURIEUX
        "👀 Le Corps Humain": { "Visage & Corps": {"👀":"Yeux","👂":"Oreilles","👃":"Nez","👄":"Bouche","🦷":"Dents","🖐️":"Main","🦶":"Pied","💪":"Bras","🦵":"Jambe"} },
        "🪐 Système Solaire": { "L'Espace": {"☀️":"Soleil","🌍":"Terre","🌙":"Lune","🔴":"Mars","🪐":"Saturne","⭐":"Étoile filante","☄️":"Comète"} },
        "☀️ Météo": { "Le Temps": {"☀️":"Soleil","☁️":"Nuage","🌧️":"Pluie","⚡":"Orage","❄️":"Neige","🌪️":"Tornade","🌈":"Arc-en-ciel"} },
        "🍎 Le Marché": {
            "Fruits": {"🍎":"Pomme","🍌":"Banane","🍓":"Fraise","🍉":"Pastèque","🍍":"Ananas","🥝":"Kiwi","🍒":"Cerise","🍑":"Pêche","🍇":"Raisin"},
            "Légumes": {"🥕":"Carotte","🥦":"Brocoli","🌽":"Maïs","🍅":"Tomate","🍆":"Aubergine","🧅":"Oignon","🥔":"Patate"}
        }
    },
    "SLIDE_5": { # 🎨 SALLE DE JEUX
        "🎨 Couleurs": { "Palette": {"🔴":"Rouge","🔵":"Bleu","🟢":"Vert","🟡":"Jaune","🟠":"Orange","🟣":"Violet","⚫":"Noir","⚪":"Blanc","🟤":"Marron","🩷":"Rose"} },
        "🎹 Musique": { "Orchestre": {"🎹":"Piano","🎸":"Guitare","🥁":"Batterie","🎺":"Trompette","🎻":"Violon","🎷":"Saxophone"} },
        "😀 Émotions": { "Comment tu te sens ?": {"😀":"Joyeux","😢":"Triste","😡":"En colère","😱":"Peur","😴":"Fatigué","🤪":"Rigolo"} },
        "🏆 Récompenses": { "Cadeaux": {"🎈":"Ballons","🎁":"Cadeau","🌟":"Étoile Magique","👑":"Couronne"} }
    }
}

# --- 6. BARRE DE NAVIGATION SUPÉRIEURE (5 POINTS) ---
st.markdown('<div class="nav-box">', unsafe_allow_html=True)
cols_nav = st.columns(5)
onglets = ["📚 École", "🦁 Nature", "🌍 Monde", "🧠 Curieux", "🎨 Jeux"]

for i in range(5):
    with cols_nav[i]:
        color = "#FF0055" if st.session_state.slide == (i+1) else "#555"
        # Le bouton utilise du HTML/CSS inline pour faire un beau point coloré
        if st.button(f"{onglets[i]}", key=f"nav_{i}"): changer_slide(i+1)
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. AFFICHAGE DYNAMIQUE ---
current_db = DATABASE[f"SLIDE_{st.session_state.slide}"]

if st.session_state.page == "home":
    st.markdown(f"<div class='titre-page'>✨ {onglets[st.session_state.slide - 1]} ✨</div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, cat in enumerate(current_db.keys()):
        with cols[i % 2]:
            if st.button(cat, key=f"cat_{cat}"): nav(cat)

elif st.session_state.page in current_db:
    if st.button("⬅️ RETOUR AUX CATÉGORIES"): nav("home")
    st.markdown(f"<div class='titre-page'>📌 {st.session_state.page}</div>", unsafe_allow_html=True)
    
    sub_data = current_db[st.session_state.page]
    
    if st.session_state.sub == "":
        cols = st.columns(2)
        for i, s in enumerate(sub_data.keys()):
            with cols[i % 2]:
                if st.button(s, key=f"sub_{s}"): nav(st.session_state.page, s)
    else:
        if st.button("⬅️ CHANGER DE SECTION"): nav(st.session_state.page, "")
        st.write("---")
        
        items = sub_data[st.session_state.sub]
        cols = st.columns(2)
        
        if isinstance(items, list):
            for i, val in enumerate(items):
                with cols[i % 2]:
                    if st.button(val, key=f"item_list_{val}_{i}"): parler(val)
        else:
            for i, (k, v) in enumerate(items.items()):
                with cols[i % 2]:
                    if st.button(f"{k} {v}", key=f"item_dict_{v}_{i}"):
                        parler(v)
                        # Animation spéciale pour les récompenses
                        if v == "Ballons" or v == "Étoile Magique":
                            st.balloons()
