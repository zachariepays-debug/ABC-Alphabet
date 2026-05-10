import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="L'Empire des Génies", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS ANIMÉ & CONTRASTE MAXIMAL ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #050505; } 
    
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-4px); } 100% { transform: translateY(0px); } }
    @keyframes slideIn { from { opacity: 0; transform: translateX(-15px); } to { opacity: 1; transform: translateX(0); } }

    .stButton > button {
        width: 100%; height: 100px !important;
        font-size: 20px !important; font-weight: 900 !important;
        border-radius: 18px !important; border: 3px solid #333 !important;
        text-transform: uppercase; 
        animation: float 3s infinite ease-in-out, slideIn 0.3s ease-out;
        transition: all 0.2s;
    }
    .stButton > button:active { transform: scale(0.9) !important; border-color: #FFF !important; }
    
    div[data-testid="stVerticalBlock"] > div:nth-child(odd) button { background: linear-gradient(135deg, #FF0055, #FF5588) !important; color: white !important; }
    div[data-testid="stVerticalBlock"] > div:nth-child(even) button { background: linear-gradient(135deg, #00CCFF, #0077FF) !important; color: white !important; }
    
    .titre-page { text-align: center; color: #FFD700; font-size: 40px !important; font-weight: 900; text-shadow: 2px 2px #FF0055; margin-bottom: 20px; animation: slideIn 0.5s; }
    .nav-box { display: flex; justify-content: center; gap: 10px; margin-bottom: 25px; background: #111; padding: 10px; border-radius: 25px; border: 2px solid #222; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ÉTATS ---
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

# --- 5. LA BASE DE DONNÉES GÉANTE (DES CENTAINES D'ENTRÉES) ---
DATABASE = {
    "SLIDE_1": { # 📚 ÉCOLE
        "🔤 Alphabet": { "Lettres de A à Z": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") },
        "🔢 Chiffres": { "0 à 50": [str(i) for i in range(51)], "51 à 100": [str(i) for i in range(51, 101)] },
        "📐 Formes": { "Géométrie": {"🟦":"Carré","🔴":"Rond","🔺":"Triangle","⭐":"Étoile","💎":"Losange","❤️":"Cœur","🟩":"Rectangle","🛑":"Octogone","🌙":"Croissant","⬟":"Pentagone"} },
        "📅 Le Temps": {
            "Les Jours": {"1":"Lundi","2":"Mardi","3":"Mercredi","4":"Jeudi","5":"Vendredi","6":"Samedi","7":"Dimanche"},
            "Les Mois": {"Jan":"Janvier","Fév":"Février","Mar":"Mars","Avr":"Avril","Mai":"Mai","Juin":"Juin","Juil":"Juillet","Août":"Août","Sep":"Septembre","Oct":"Octobre","Nov":"Novembre","Déc":"Décembre"},
            "Saisons": {"🌸":"Printemps","☀️":"Été","🍂":"Automne","❄️":"Hiver"}
        },
        "➕ Calculs": { 
            "Additions": {"1+1=":"2","2+2=":"4","3+3=":"6","4+4=":"8","5+5=":"10","10+10=":"20"}, 
            "Soustractions": {"2-1=":"1","5-2=":"3","10-5=":"5","10-1=":"9"} 
        },
        "🎨 Couleurs": { "Nuances": {"🔴":"Rouge","🔵":"Bleu","🟢":"Vert","🟡":"Jaune","🟠":"Orange","🟣":"Violet","⚫":"Noir","⚪":"Blanc","🟤":"Marron","🩷":"Rose","🩶":"Gris","🩵":"Cyan"} }
    },
    "SLIDE_2": { # 🦁 NATURE
        "🦖 Dinosaures": {
            "Carnivores": {"🦖 T-Rex":"Tyrannosaure","🦖 Raptor":"Vélociraptor","🦖 Spino":"Spinosaure","🦖 Allosaure":"Allosaure","🦖 Carno":"Carnotaure"},
            "Herbivores": {"🦕 Diplo":"Diplodocus","🦕 Tricé":"Tricératops","🦕 Stego":"Stégosaure","🦕 Brachio":"Brachiosaure","🦕 Ankylo":"Ankylosaure","🦕 Iguanodon":"Iguanodon"},
            "Volants & Marins": {"🕊️ Ptéro":"Ptérodactyle","🌊 Mosa":"Mosasaurus","🌊 Plésio":"Plésiosaure","🌊 Ichtio":"Ichthyosaure"}
        },
        "🦁 Zoo & Savane": { "Animaux": {"🦁":"Lion","🐘":"Éléphant","🦒":"Girafe","🦓":"Zèbre","🐵":"Singe","🦛":"Hippopotame","🦏":"Rhinocéros","🐆":"Léopard","🦍":"Gorille","🐯":"Tigre","🐆":"Guépard","hyène":"Hyène","🐊":"Crocodile","🐍":"Serpent","🐪":"Chameau","🐫":"Dromadaire","🦘":"Kangourou","🐼":"Panda","🦥":"Paresseux"} },
        "🐟 Océan & Eau": { "Marins": {"🐬":"Dauphin","🐋":"Baleine","🦈":"Requin","🐙":"Poulpe","🐢":"Tortue marine","🦀":"Crabe","🦞":"Homard","🐠":"Poisson tropical","🐡":"Poisson lune","🦑":"Calamar","🦭":"Phoque","🐧":"Pingouin","🦦":"Loutre","🦪":"Huître","🐚":"Coquillage","🦐":"Crevette"} },
        "🐷 Ferme & Forêt": { "Campagne": {"🐮":"Vache","🐷":"Cochon","🐔":"Poule","🦆":"Canard","🐴":"Cheval","🐑":"Mouton","🐰":"Lapin","🐶":"Chien","🐱":"Chat","🐐":"Chèvre","🦃":"Dindon","🦢":"Cygne","🦊":"Renard","🦌":"Cerf","🐺":"Loup","🐻":"Ours","🐿️":"Écureuil","🦉":"Hibou","🦔":"Hérisson","🦇":"Chauve-souris"} },
        "🐞 Insectes": { "Petites bêtes": {"🦋":"Papillon","🐝":"Abeille","🐞":"Coccinelle","🐜":"Fourmi","🕷️":"Araignée","🐛":"Chenille","🐌":"Escargot","🦟":"Moustique","🦗":"Criquet","🪲":"Scarabée","🦂":"Scorpion","🪱":"Ver de terre"} },
        "🌳 Végétaux": { "Plantes": {"🌳":"Arbre","🌲":"Sapin","🌴":"Palmier","🌵":"Cactus","🌹":"Rose","🌻":"Tournesol","🌷":"Tulipe","🍄":"Champignon","🍀":"Trèfle","🌿":"Feuille"} }
    },
    "SLIDE_3": { # 🌍 MONDE
        "🌍 Drapeaux Europe": { "Europe": {"🇫🇷":"France","🇧🇪":"Belgique","🇨🇭":"Suisse","🇮🇹":"Italie","🇪🇸":"Espagne","🇩🇪":"Allemagne","🇬🇧":"Royaume-Uni","🇵🇹":"Portugal","🇳🇱":"Pays-Bas","🇬🇷":"Grèce","🇷🇺":"Russie","🇸🇪":"Suède","🇳🇴":"Norvège","🇫🇮":"Finlande","🇩🇰":"Danemark","🇮🇪":"Irlande","🇦🇹":"Autriche","🇵🇱":"Pologne","🇺🇦":"Ukraine","🇨🇿":"Tchéquie"} },
        "🌍 Drapeaux Afrique": { "Afrique": {"🇲🇦":"Maroc","🇩🇿":"Algérie","🇹🇳":"Tunisie","🇸🇳":"Sénégal","🇨🇮":"Côte d'Ivoire","🇨🇲":"Cameroun","🇲🇱":"Mali","🇪🇬":"Égypte","🇿🇦":"Afrique du Sud","🇲🇬":"Madagascar","🇰🇪":"Kenya","🇳🇬":"Nigeria","🇬🇭":"Ghana","🇦🇴":"Angola","🇨🇩":"Congo","🇪🇹":"Éthiopie"} },
        "🌍 Drapeaux Amériques": { "Amériques": {"🇨🇦":"Canada","🇺🇸":"États-Unis","🇲🇽":"Mexique","🇧🇷":"Brésil","🇦🇷":"Argentine","🇨🇴":"Colombie","🇨🇱":"Chili","🇵🇪":"Pérou","🇨🇺":"Cuba","🇻🇪":"Venezuela","🇺🇾":"Uruguay","🇪🇨":"Équateur","🇯🇲":"Jamaïque","🇧🇴":"Bolivie"} },
        "🌍 Drapeaux Asie": { "Asie & Océanie": {"🇯🇵":"Japon","🇨🇳":"Chine","🇰🇷":"Corée du Sud","🇮🇳":"Inde","🇦🇺":"Australie","🇹🇭":"Thaïlande","🇻🇳":"Vietnam","🇮🇩":"Indonésie","🇵🇭":"Philippines","🇳🇿":"Nouvelle-Zélande","🇸🇬":"Singapour","🇲🇾":"Malaisie"} },
        "🚀 Transports": {
            "Route": {"🚗":"Voiture","🚓":"Voiture de police","🚒":"Camion de pompier","🚑":"Ambulance","🚌":"Bus","🚜":"Tracteur","🚚":"Camion","🚲":"Vélo","🏍️":"Moto","🛴":"Trottinette","🛹":"Skateboard"},
            "Air & Eau & Rail": {"✈️":"Avion","🚀":"Fusée","🚁":"Hélicoptère","🛸":"Soucoupe","🚢":"Bateau","🛶":"Canoë","🛳️":"Paquebot","🚤":"Hors-bord","🚂":"Train","🚄":"TGV","🚃":"Tramway","🚠":"Téléphérique"}
        },
        "🧑‍⚕️ Métiers": { "Professions": {"🚒":"Pompier","👮":"Policier","🧑‍⚕️":"Docteur","🧑‍🍳":"Cuisinier","🧑‍🚀":"Astronaute","🧑‍🏫":"Professeur","🧑‍🔧":"Mécanicien","🧑‍🌾":"Fermier","👩‍⚖️":"Juge","👷":"Ouvrier","🎨":"Peintre","🎶":"Musicien","🕵️":"Détective","👨‍✈️":"Pilote","👨‍🔬":"Scientifique","👨‍🚒":"Garde forestier"} },
        "🏠 La Maison": { 
            "Pièces & Meubles": {"🛌":"Lit","🛋️":"Canapé","🪑":"Chaise","🚪":"Porte","🪟":"Fenêtre","🛁":"Baignoire","🚽":"Toilettes","🚿":"Douche"},
            "Objets": {"📺":"Télévision","📱":"Téléphone","💻":"Ordinateur","🔑":"Clé","🧸":"Jouet","🕰️":"Horloge","🧺":"Panier","🗑️":"Poubelle"},
            "Cuisine": {"🍽️":"Assiette","🍴":"Fourchette","🥄":"Cuillère","🔪":"Couteau","🧊":"Glaçon","🍳":"Poêle","🧂":"Sel"}
        }
    },
    "SLIDE_4": { # 🧠 CURIEUX
        "👀 Corps Humain": { "Anatomie": {"👀":"Yeux","👂":"Oreilles","👃":"Nez","👄":"Bouche","🦷":"Dents","👅":"Langue","🧠":"Cerveau","🦴":"Os","🖐️":"Main","🦶":"Pied","💪":"Bras","🦵":"Jambe","🫀":"Cœur","🫁":"Poumons"} },
        "🪐 Espace": { "Univers": {"☀️":"Soleil","🌍":"Terre","🌙":"Lune","🔴":"Mars","🪐":"Saturne","🌑":"Mercure","🌕":"Vénus","🔵":"Neptune","⭐":"Étoile filante","☄️":"Comète","🌌":"Galaxie","🔭":"Télescope","👽":"Extraterrestre"} },
        "☀️ Météo": { "Climat": {"☀️":"Soleil","☁️":"Nuage","⛅":"Éclaircie","🌧️":"Pluie","⛈️":"Orage","⚡":"Éclair","❄️":"Neige","☃️":"Bonhomme de neige","🌪️":"Tornade","🌫️":"Brouillard","🌈":"Arc-en-ciel","🌬️":"Vent"} },
        "🍎 Fruits": { "Le Verger": {"🍎":"Pomme","🍌":"Banane","🍓":"Fraise","🍉":"Pastèque","🍍":"Ananas","🥝":"Kiwi","🍒":"Cerise","🍑":"Pêche","🍇":"Raisin","🍈":"Melon","🍊":"Orange","🍋":"Citron","🍐":"Poire","🥭":"Mangue","🥥":"Noix de coco","🥑":"Avocat","🫐":"Myrtille"} },
        "🥦 Légumes": { "Le Potager": {"🥕":"Carotte","🥦":"Brocoli","🌽":"Maïs","🍅":"Tomate","🍆":"Aubergine","🧅":"Oignon","🥔":"Patate","🧄":"Ail","🥒":"Concombre","🥬":"Salade","🫑":"Poivron","🍠":"Patate douce","🫛":"Petit pois","🍄":"Champignon"} },
        "🍔 Nourriture": { "Plats": {"🥖":"Pain","🥐":"Croissant","🧀":"Fromage","🥚":"Œuf","🥞":"Crêpe","🍕":"Pizza","🍔":"Hamburger","🍟":"Frites","🌭":"Hot-dog","🍝":"Pâtes","🍜":"Nouilles","🍚":"Riz","🍣":"Sushi","🍦":"Glace","🍩":"Donut","🍪":"Cookie","🍫":"Chocolat","🍬":"Bonbon","🍯":"Miel"} }
    },
    "SLIDE_5": { # 🎨 JEUX
        "🎹 Musique": { "Instruments": {"🎹":"Piano","🎸":"Guitare","🥁":"Batterie","🎺":"Trompette","🎻":"Violon","🎷":"Saxophone","🪗":"Accordéon","🪕":"Banjo","🪘":"Tam-tam","🎤":"Micro","🎧":"Casque audio"} },
        "⚽ Sports": { "Activités": {"⚽":"Football","🏀":"Basketball","🎾":"Tennis","🏐":"Volleyball","🏉":"Rugby","⚾":"Baseball","🥊":"Boxe","🥋":"Judo","🎿":"Ski","🏂":"Snowboard","⛸️":"Patinage","🏊":"Natation","🚴":"Cyclisme","🏹":"Tir à l'arc","🎣":"Pêche"} },
        "😀 Émotions": { "Sentiments": {"😀":"Joyeux","😂":"Mort de rire","😊":"Souriant","🥰":"Amoureux","😎":"Cool","🤔":"Réflechi","😐":"Neutre","😢":"Triste","😭":"En pleurs","😡":"En colère","🤬":"Furieux","😱":"Peur","😴":"Fatigué","🥱":"Baille","🤢":"Malade","🤪":"Fou fou","🤫":"Chut"} },
        "👗 Vêtements": { "Garde-robe": {"👕":"T-shirt","👖":"Pantalon","👗":"Robe","🧥":"Manteau","🧣":"Écharpe","🧤":"Gants","🧦":"Chaussettes","👟":"Baskets","👞":"Chaussures","👒":"Chapeau","🧢":"Casquette","👑":"Couronne","🎒":"Sac à dos","🥽":"Lunettes"} },
        "🎉 Récompenses (Magie)": { "Cadeaux": {"🎈":"Ballons","🎁":"Cadeau","🌟":"Étoile Magique","👑":"Super Champion","🏆":"Coupe en or","🥇":"Médaille","💎":"Diamant","🪄":"Baguette magique","🎊":"Fête"} }
    }
}

# --- 6. NAVIGATION ---
st.markdown('<div class="nav-box">', unsafe_allow_html=True)
cols_nav = st.columns(5)
onglets = ["📚 ÉCOLE", "🦁 NATURE", "🌍 MONDE", "🧠 CURIEUX", "🎨 JEUX"]

for i in range(5):
    with cols_nav[i]:
        if st.button(f"{onglets[i]}", key=f"nav_{i}"): changer_slide(i+1)
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. AFFICHAGE ---
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
        
        # Adaptation du nombre de colonnes si la liste est immense (pour plus de visibilité)
        num_cols = 3 if isinstance(items, list) and len(items) > 10 else 2
        cols = st.columns(num_cols)
        
        if isinstance(items, list):
            for i, val in enumerate(items):
                with cols[i % num_cols]:
                    if st.button(val, key=f"item_list_{val}_{i}"): parler(val)
        else:
            for i, (k, v) in enumerate(items.items()):
                with cols[i % num_cols]:
                    if st.button(f"{k} {v}", key=f"item_dict_{v}_{i}"):
                        parler(v)
                        # Magie des récompenses
                        if v in ["Ballons", "Fête", "Cadeau", "Super Champion", "Étoile Magique"]:
                            st.balloons()
