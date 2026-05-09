import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="App Bébé Éducative", page_icon="👶", layout="centered")

# --- 2. SYSTÈME DE VÉROUILLAGE PAR URL ---
# On vérifie si l'utilisateur a tapé ?admin=babar à la fin de l'adresse
is_admin = st.query_params.get("admin") == "babar"

if not is_admin:
    # ÉCRAN NOIR POUR TOUT LE MONDE
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 25px;'>L'application revient très vite avec des nouveautés ! ✨</p>", unsafe_allow_html=True)
    st.stop() # Arrête le code ici pour les gens sans le lien spécial

# --- 3. FONCTION SON (TTS) ---
def parler(texte):
    try:
        tts = gTTS(text=str(texte), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_b64 = base64.b64encode(fp.getvalue()).decode()
        html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
        st.markdown(html_string, unsafe_allow_html=True)
    except:
        pass

# --- 4. INTERFACE NORMALE (VISIBLE UNIQUEMENT PAR ADMIN) ---
st.title("👶 Mon Abécédaire Magique")
st.success("Accès Administrateur Activé ✅")

# Style des boutons pour qu'ils soient gros et carrés
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 22px !important;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    st.subheader("Les lettres (A-Z)")
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # Affichage ligne par ligne (6 colonnes) pour garder l'ordre
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"L_{lettre}"):
                    parler(lettre)

with tab2:
    st.subheader("Les chiffres (0-9)")
    chiffres = list("0123456789")
    # Affichage ligne par ligne (5 colonnes)
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"C_{chiffre}"):
                    parler(chiffre)
