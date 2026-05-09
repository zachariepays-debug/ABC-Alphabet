import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="App Bébé Éducative", page_icon="👶", layout="centered")

# --- 2. SYSTÈME DE MAINTENANCE (KILL SWITCH) ---
if "maintenance" in st.query_params and st.query_params["maintenance"] == "true":
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 25px;'>Reviens bientôt, on prépare des surprises ! ✨</p>", unsafe_allow_html=True)
    
    unlock = st.text_input("Code secret pour réouvrir", type="password")
    if unlock == "babar":
        st.query_params.clear()
        st.rerun()
    st.stop()

# --- 3. FONCTION SON ---
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

# --- 4. BOUTON ADMIN ---
c1, c2 = st.columns([0.9, 0.1])
with c2:
    if st.button("Admin"):
        st.session_state.show_admin = not st.session_state.get('show_admin', False)

if st.session_state.get('show_admin', False):
    with st.expander("🔐 Contrôle", expanded=True):
        pwd = st.text_input("Mot de passe", type="password")
        if pwd == "babar":
            if st.button("🔴 BLOQUER L'APPLI (Maintenance)"):
                st.query_params["maintenance"] = "true"
                st.rerun()

# --- 5. INTERFACE PRINCIPALE ---
st.title("👶 Mon Abécédaire Magique")

# Style pour des boutons carrés et bien rangés
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 22px !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    st.subheader("Les lettres (A-Z)")
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # On crée des lignes de 6 colonnes
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"lettre_{lettre}"):
                    parler(lettre)

with tab2:
    st.subheader("Les chiffres (0-9)")
    chiffres = list("0123456789")
    # On crée des lignes de 5 colonnes
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"chiffre_{chiffre}"):
                    parler(chiffre)
