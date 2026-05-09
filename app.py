import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="App Bébé Éducative", page_icon="👶", layout="centered")

# --- 2. FONCTION POUR LE SON ---
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

# --- 3. MENU ADMIN (DISCRET) ---
col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("Admin", key="admin_btn"):
        st.session_state.show_admin = not st.session_state.get('show_admin', False)

if st.session_state.get('show_admin', False):
    with st.expander("🔐 Panneau de contrôle", expanded=True):
        pwd = st.text_input("Mot de passe admin", type="password")
        if pwd == "babar":
            st.success("Accès Admin activé")
            st.write("Ici, tu pourras ajouter tes futurs réglages !")
            if st.button("Fermer le menu"):
                st.session_state.show_admin = False
                st.rerun()

# --- 4. INTERFACE PRINCIPALE ---
st.title("👶 Mon Abécédaire Magique")
st.write("Clique sur une lettre ou un chiffre pour l'entendre !")

# Style des boutons
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
    # On affiche par lignes de 6 pour que ce soit bien rangé
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"L_{lettre}"):
                    parler(lettre)

with tab2:
    st.subheader("Les chiffres (0-9)")
    chiffres = list("0123456789")
    # On affiche par lignes de 5
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"C_{chiffre}"):
                    parler(chiffre)
