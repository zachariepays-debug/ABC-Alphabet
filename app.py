import streamlit as st
from gtts import gTTS
import base64
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="App Bébé", page_icon="👶")

# --- INITIALISATION DE L'ACCÈS ---
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

# --- ÉCRAN DE BLOCAGE ---
if not st.session_state.access_granted:
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.write("### L'application revient très vite avec des nouveautés ! ✨")
    
    # LA BARRE POUR DÉBLOQUER
    code = st.text_input("Entrez le code pour débloquer", type="password")
    if code == "babar":
        st.session_state.access_granted = True
        st.rerun()
    st.stop()

# --- FONCTION SON ---
def parler(texte):
    tts = gTTS(text=str(texte), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    audio_b64 = base64.b64encode(fp.getvalue()).decode()
    html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
    st.markdown(html_string, unsafe_allow_html=True)

# --- INTERFACE (VISIBLE APRÈS DÉBLOCAGE) ---
col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("🔴 Re-bloquer"):
        st.session_state.access_granted = False
        st.rerun()

st.title("👶 Mon Abécédaire Magique")

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
