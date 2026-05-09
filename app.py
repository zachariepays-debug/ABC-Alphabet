import streamlit as st
from gtts import gTTS
import base64
import io

# 1. INITIALISATION DE L'ÉTAT (Pour bloquer/débloquer l'app)
if 'maintenance' not in st.session_state:
    st.session_state.maintenance = False

# --- MODE MAINTENANCE (Ce que tout le monde voit si c'est bloqué) ---
if st.session_state.maintenance:
    st.markdown("""
        <style>
        stApp { background-color: black; color: white; }
        .main { background-color: #000000; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>🛠️ MISE À JOUR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>L'application est en cours de maintenance stylée... ✨</p>", unsafe_allow_html=True)
    
    # Barre pour réactiver
    unlock_pass = st.text_input("Code de réactivation", type="password")
    if unlock_pass == "babar":
        st.session_state.maintenance = False
        st.rerun()
    st.stop() # Arrête le reste du code ici

# --- CODE DE L'APPLICATION NORMALE ---
st.set_page_config(page_title="App Bébé", page_icon="👶")

def parler(texte):
    tts = gTTS(text=str(texte), lang='fr')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    audio_b64 = base64.b64encode(fp.getvalue()).decode()
    html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
    st.markdown(html_string, unsafe_allow_html=True)

# PETIT BOUTON ADMIN DISCRET EN HAUT À DROITE
col1, col2 = st.columns([0.9, 0.1])
with col2:
    if st.button("Admin"):
        st.session_state.show_admin = True

# FENÊTRE ADMIN (S'affiche si on a cliqué sur Admin)
if st.session_state.get('show_admin', False):
    with st.expander("Zone Administrateur", expanded=True):
        password = st.text_input("Mot de passe", type="password")
        if password == "babar":
            st.success("Accès autorisé")
            if st.button("🔴 FERMER L'APPLICATION (Mode Mise à jour)"):
                st.session_state.maintenance = True
                st.rerun()
            if st.button("Fermer ce menu"):
                st.session_state.show_admin = False
                st.rerun()
        elif password != "":
            st.error("Mauvais mot de passe")

st.title("👶 Mon App Éducative")

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    st.subheader("Apprends les lettres")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = st.columns(6)
    for i, lettre in enumerate(alphabet):
        with cols[i % 6]:
            if st.button(lettre, key=f"btn_{lettre}"):
                parler(lettre)

with tab2:
    st.subheader("Apprends les chiffres")
    chiffres = "0123456789"
    cols_c = st.columns(5)
    for i, chiffre in enumerate(chiffres):
        with cols_c[i % 5]:
            if st.button(chiffre, key=f"btn_{chiffre}"):
                parler(chiffre)
