import streamlit as st
from gtts import gTTS
import base64
import io

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="App Bébé Éducative", page_icon="👶", layout="centered")

# --- 2. SYSTÈME DE BLOCAGE (MAINTENANCE) ---
# On utilise les query_params pour que le blocage soit visible via l'URL
if "maintenance" in st.query_params and st.query_params["maintenance"] == "true":
    st.markdown("""
        <style>
        .stApp { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='color: red; text-align: center; font-size: 50px;'>🛠️ MISE À JOUR EN COURS</h1>", unsafe_allow_html=True)
    st.write("### L'administrateur prépare des nouveautés... ✨")
    
    # Barre de déblocage
    unlock = st.text_input("Entrez le mot de passe pour réouvrir", type="password")
    if unlock == "babar":
        st.query_params.clear() # On vide l'URL pour réouvrir l'app
        st.rerun()
    st.stop() # On arrête l'exécution ici pour que personne ne voit l'app

# --- 3. FONCTIONS UTILES ---
def parler(texte):
    """Génère et joue le son de la lettre ou du chiffre"""
    try:
        tts = gTTS(text=str(texte), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_b64 = base64.b64encode(fp.getvalue()).decode()
        html_string = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
        st.markdown(html_string, unsafe_allow_html=True)
    except:
        st.error("Erreur de son")

# --- 4. INTERFACE ADMIN DISCRÈTE ---
col1, col2 = st.columns([0.9, 0.1])
with col2:
    # Petit bouton discret en haut à droite
    if st.button("Admin", key="admin_btn"):
        st.session_state.show_admin = not st.session_state.get('show_admin', False)

if st.session_state.get('show_admin', False):
    with st.expander("🔐 Panneau de contrôle", expanded=True):
        pwd = st.text_input("Mot de passe admin", type="password")
        if pwd == "babar":
            st.success("Accès Admin activé")
            if st.button("🔴 FERMER L'APPLI POUR TOUS"):
                st.query_params["maintenance"] = "true"
                st.rerun()
        elif pwd != "":
            st.error("Mot de passe incorrect")

# --- 5. CONTENU DE L'APPLICATION ---
st.title("👶 Mon Abécédaire Magique")
st.write("Clique sur une touche pour apprendre !")

# Style des boutons (gros et colorés)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 3em;
        width: 3em;
        font-size: 24px;
        font-weight: bold;
        border-radius: 15px;
        background-color: #f0f2f6;
        border: 2px solid #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = st.columns(6)
    for i, lettre in enumerate(alphabet):
        with cols[i % 6]:
            if st.button(lettre, key=f"L_{lettre}"):
                parler(lettre)

with tab2:
    chiffres = "0123456789"
    cols_c = st.columns(5)
    for i, chiffre in enumerate(chiffres):
        with cols_c[i % 5]:
            if st.button(chiffre, key=f"C_{chiffre}"):
                parler(chiffre)
