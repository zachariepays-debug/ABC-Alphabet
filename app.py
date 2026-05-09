import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. VÉRIFICATION DU BLOCAGE GLOBAL ---
# L'appli vérifie dans les secrets si elle doit se couper
# Si maintenance_mode n'existe pas ou est "off", l'appli reste ouverte.
if st.secrets.get("maintenance_mode") == "on":
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 25px;'>Reviens plus tard ! ✨</p>", unsafe_allow_html=True)
    st.stop()

# --- 2. CONFIGURATION DE L'APPLI ---
st.set_page_config(page_title="App Bébé", page_icon="👶")

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

# --- 3. COIN ADMIN DISCRET ---
col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("Admin", key="btn_admin"):
        st.session_state.show_admin = not st.session_state.get('show_admin', False)

if st.session_state.get('show_admin', False):
    with st.expander("🔐 Zone Admin", expanded=True):
        pwd = st.text_input("Mot de passe", type="password")
        if pwd == "babar":
            st.warning("Pour BLOQUER l'appli sur TOUS les téléphones :")
            st.write("1. Va dans Settings > Secrets sur Streamlit")
            st.write("2. Écris : maintenance_mode = 'on'")
            if st.button("Fermer ce menu"):
                st.session_state.show_admin = False
                st.rerun()

# --- 4. L'ALPHABET ET LES CHIFFRES ---
st.title("👶 Mon Abécédaire")

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
