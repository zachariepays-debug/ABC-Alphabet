import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import io
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="App Bébé avec Comptes", page_icon="👶")

# --- PARAMÈTRES GITHUB (À REMPLIR DANS LES SECRETS PLUS TARD) ---
# Pour l'instant, on utilise une simulation locale pour que tu puisses tester
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"admin": "babar"} # Compte par défaut

# --- FONCTIONS ---
def parler(texte):
    try:
        tts = gTTS(text=str(texte), lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">', unsafe_allow_html=True)
    except: pass

# --- GESTION DE LA CONNEXION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    menu = ["Connexion", "Inscription"]
    choix = st.sidebar.selectbox("Menu", menu)

    if choix == "Inscription":
        st.subheader("Créer un compte")
        new_user = st.text_input("Nom d'utilisateur")
        new_pwd = st.text_input("Mot de passe", type="password")
        if st.button("S'inscrire"):
            st.session_state.users_db[new_user] = new_pwd
            st.success("Compte créé ! Connecte-toi maintenant.")
            
    else:
        st.subheader("Se connecter")
        user = st.text_input("Nom d'utilisateur")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            if user in st.session_state.users_db and st.session_state.users_db[user] == pwd:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("Identifiants incorrects")
    st.stop()

# --- SI CONNECTÉ : L'APPLICATION ---
st.sidebar.write(f"Utilisateur : **{st.session_state.current_user}**")
if st.sidebar.button("Déconnexion"):
    st.session_state.logged_in = False
    st.rerun()

# --- COIN ADMIN ---
if st.session_state.current_user == "admin":
    with st.expander("🔐 COIN ADMIN (Liste des comptes)"):
        st.write("Voici tous les utilisateurs inscrits :")
        df = pd.DataFrame(st.session_state.users_db.items(), columns=['Identifiant', 'Mot de Passe'])
        st.table(df)

# --- CONTENU ---
st.title("👶 Mon Abécédaire Magique")
tab1, tab2 = st.tabs(["🔤 Alphabet", "🔢 Chiffres"])

with tab1:
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i in range(0, len(alphabet), 6):
        cols = st.columns(6)
        for j, lettre in enumerate(alphabet[i:i+6]):
            with cols[j]:
                if st.button(lettre, key=f"L_{lettre}"): parler(lettre)

with tab2:
    chiffres = list("0123456789")
    for i in range(0, len(chiffres), 5):
        cols = st.columns(5)
        for j, chiffre in enumerate(chiffres[i:i+5]):
            with cols[j]:
                if st.button(chiffre, key=f"C_{chiffre}"): parler(chiffre)
