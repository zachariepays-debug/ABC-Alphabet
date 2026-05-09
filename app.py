import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. SYSTÈME DE BLOCAGE "LIEN MAGIQUE" ---
# Si l'URL ne contient pas "?admin=babar", on affiche l'écran noir
is_admin = st.query_params.get("admin") == "babar"

if not is_admin:
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.write("### L'application arrive bientôt ! ✨")
    st.stop()

# --- 2. SI TU ES ADMIN (Lien correct), L'APPLI S'AFFICHE ---
st.set_page_config(page_title="App Bébé", page_icon="👶")

def parler(texte):
    tts = gTTS(text=str(texte), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    audio_b64 = base64.b64encode(fp.getvalue()).decode()
    html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
    st.markdown(html_string, unsafe_allow_html=True)

st.title("👶 Mode Administrateur Activé")
st.write("Tu es le seul à voir l'appli car tu as le bon lien.")

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"L_{lettre}"):
                    parler(lettre)

with tab2:
    chiffres = list("0123456789")
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"C_{chiffre}"):
                    parler(chiffre)
